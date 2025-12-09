import os
import tempfile

from flask import Flask, jsonify, render_template, request, send_file
from services.markdown_converter import MarkdownConverter
from services.pdf_converter import PdfConverter
from constants.constants import GENERATED_FOLDER, PORT

app = Flask(__name__)

@app.route('/import_markdown', methods=['POST'])
def import_markdown():
    # Should call a specific file that will handle the import of the markdown file
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    # Temporary save the file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".md") as tmp:
        file.save(tmp.name)
        tmp_path = tmp.name

    md_converter = MarkdownConverter()
    html_output = md_converter.convert_file(tmp_path)

    # Clean the temporary file
    os.remove(tmp_path)
    
    return jsonify({'html_output': html_output}), 200

@app.route('/export_pdf', methods=['POST'])
def export_pdf():
    html_content = request.form.get("html")
    if not html_content:
        return "No HTML provided", 400

    converter = PdfConverter(style="lightbulb")
    pdf_path = converter.generate_pdf(html_content)

    return send_file(pdf_path, as_attachment=True, download_name="report.pdf")

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=PORT)
