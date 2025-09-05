from bs4 import BeautifulSoup
from pygments import highlight
from pygments.lexers import get_lexer_by_name, TextLexer, guess_lexer
from pygments.formatters import HtmlFormatter
from weasyprint import HTML
from flask import render_template

class PdfConverter:
    def __init__(self, style="colorful"):
        self.style = style
        self.pygments_css = HtmlFormatter(style=self.style).get_style_defs(".highlight")

    def apply_pygments(self, quill_html: str) -> str:
        soup = BeautifulSoup(quill_html, "html.parser")
        formatter = HtmlFormatter(style=self.style)

        for pre_tag in soup.find_all("pre"):
            code_tag = pre_tag.find("code")
            if not code_tag:
                continue

            code_text = code_tag.get_text()
            
            # Language
            try:
                # Get lexer thanks to the class language-<language>
                language = code_tag.get("class", "text")[0].split("-")[1]

                if (language == "auto"):
                    lexer = guess_lexer(code_text)
                else:
                    lexer = get_lexer_by_name(language)
            except Exception:
                lexer = TextLexer()

            # Highlight
            highlighted_html = highlight(code_text, lexer, formatter)            
            highlight_soup = BeautifulSoup(highlighted_html, "html.parser")

            pre_tag.replace_with(highlight_soup)

        return str(soup)


    def quill_to_pygments_html(self, quill_html: str) -> str:
        """
        Transform the Quill HTML to Pygments HTML.
        """
        soup = BeautifulSoup(quill_html, "html.parser")
        
        containers = soup.find_all("div", class_="ql-code-block-container")

        for container in containers:
            first_line = container.find("div", class_="ql-code-block")
            language = first_line.get("data-language", "text") if first_line else "text"

            code_lines = [line.get_text() for line in container.find_all("div", class_="ql-code-block")]
            code_text = "\n".join(code_lines)

            new_code_tag = soup.new_tag("pre")
            code_tag = soup.new_tag("code", **{"class": f"language-{language}"})
            code_tag.string = code_text
            new_code_tag.append(code_tag)

            container.replace_with(new_code_tag)

        return str(soup)

    def quill_to_highlighted_html(self, quill_html: str) -> str:
        """
        Transform the Quill HTML to highlighted HTML.
        """
        html = self.quill_to_pygments_html(quill_html)
        return self.apply_pygments(html)

    def generate_pdf(self, quill_html: str, output_path: str = None) -> str:
        """
        Convert the Quill HTML to PDF with syntax highlighting.
        """

        html_content = self.quill_to_highlighted_html(quill_html)

        rendered_html = render_template(
            "pdf_template.html",
            content=html_content,
            pygments_css=self.pygments_css
        )

        if not output_path:
            import tempfile
            tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
            output_path = tmp_file.name

        HTML(string=rendered_html).write_pdf(output_path)
        return output_path
