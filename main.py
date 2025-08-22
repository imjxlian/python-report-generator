from converters.code_wrapper import CodeWrapper
from converters.md_to_html import MarkdownConverter
from converters.html_template import HtmlTemplate
from converters.html_to_pdf import PdfConverter
import sys
import os

GENERATED_FOLDER = "generated"
FONT_SIZE_PX = 12
PAGE_WIDTH_CM = 21 # A4 width in cm
PAGE_HEIGHT_CM = 29.7 # A4 height in cm
MARGIN_CM = 2
CM_PX_RATIO = 60 # Defined manually

if __name__ == "__main__":

    # Create the tmp folder if it doesn't exist
    if not os.path.exists(GENERATED_FOLDER):
        os.makedirs(GENERATED_FOLDER)
    
    # Read the input file from the command line
    if (len(sys.argv) < 2):
        print("Usage: python main.py <input_file>")
        sys.exit(1)

    input_file = sys.argv[1]

    with open(input_file, "r", encoding="utf-8") as f:
        content = f.read()

    # Wrap and format the code blocks
    available_space_cm = PAGE_WIDTH_CM - (2 * MARGIN_CM)
    wrapper = CodeWrapper(FONT_SIZE_PX, available_space_cm, CM_PX_RATIO)
    wrapped_content = wrapper.wrap_code_blocks(content)

    # Markdown -> HTML
    md_converter = MarkdownConverter()
    html_content = md_converter.convert(wrapped_content)

    # Template
    footer_size_cm = FONT_SIZE_PX / 60
    footer_position = PAGE_HEIGHT_CM - (MARGIN_CM / 2) - footer_size_cm
    template_engine = HtmlTemplate(css = md_converter.pygments_css, body_font_size = str(FONT_SIZE_PX) + 'px', page_margin = str(MARGIN_CM) + 'cm', footer_position = str(footer_position) + 'cm', code_font_size = str(FONT_SIZE_PX) + "px")
    final_html = template_engine.build(html_content)

    # Replace leading spaces in codehilite (to avoid PDF layout issues)
    final_html = template_engine.replace_leading_spaces_in_codehilite(final_html)

    if ("--html" in sys.argv):    # If there is a --html flag, save the HTML output
        with open(f"{GENERATED_FOLDER}/output.html", "w", encoding="utf-8") as f:
            f.write(final_html)

    # HTML -> PDF
    pdf_converter = PdfConverter()
    if pdf_converter.convert(final_html, f"{GENERATED_FOLDER}/output.pdf"):
        print("✅ PDF generated : output.pdf")
    else:
        print("❌ Error when creating the PDF")
