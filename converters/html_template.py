import re


class HtmlTemplate:
    def __init__(self, css: str, 
                 page_size: str = "A4",
                 page_margin: str = "2cm",
                 footer_position: str = "28.3cm",
                 body_font_family: str = "Arial, sans-serif",
                 body_font_size: str = "12px",
                 body_line_height: str = "1",
                 code_font_family: str = '"JetBrains Mono", monospace',
                 code_font_size: str = "12px",
                 code_line_height: str = "1.3",
                 code_padding: str = "12px",
                 code_border: str = "1px solid grey",
                 footer_color: str = "#bbb"):
        self.css = css
        self.page_size = page_size
        self.page_margin = page_margin
        self.footer_position = footer_position
        self.body_font_family = body_font_family
        self.body_font_size = body_font_size
        self.body_line_height = body_line_height
        self.code_font_family = code_font_family
        self.code_font_size = code_font_size
        self.code_line_height = code_line_height
        self.code_padding = code_padding
        self.code_border = code_border
        self.footer_color = footer_color

    def _generate_page_styles(self) -> str:
        """Generate CSS styles for page layout."""
        return f"""
        @page {{
            size: {self.page_size};
            margin: {self.page_margin};
            @frame footer_frame {{
                -pdf-frame-content: footer_content;
                top: {self.footer_position};
            }}
        }}"""

    def _generate_body_styles(self) -> str:
        """Generate CSS styles for body content."""
        return f"""
        body {{
            font-family: {self.body_font_family};
            font-size: {self.body_font_size};
            line-height: {self.body_line_height};
        }}"""

    def _generate_code_styles(self) -> str:
        """Generate CSS styles for code blocks."""
        return f"""
        .codehilite {{
            font-family: {self.code_font_family};
            font-size: {self.code_font_size};
            line-height: {self.code_line_height};
            padding: {self.code_padding};
            border: {self.code_border};
        }}"""

    def _generate_layout_styles(self) -> str:
        """Generate CSS styles for page layout and breaks."""
        return """
        h1 { page-break-before: always; }
        table { page-break-inside: avoid; }
        pre { page-break-inside: avoid; }"""

    def _generate_footer(self) -> str:
        """Generate footer HTML."""
        return f"""
    <div id="footer_content" style="text-align:center;color:{self.footer_color};">
        <pdf:pagenumber>/<pdf:pagecount>
    </div>"""

    def build(self, html_content: str) -> str:
        """Build complete HTML document with styles and content."""
        template = f"""<!DOCTYPE html>
<html>
<head>
    <style>{self._generate_page_styles()}{self._generate_body_styles()}{self._generate_code_styles()}{self._generate_layout_styles()}
        {self.css}
    </style>
</head>
<body>
    {html_content}{self._generate_footer()}
</body>
</html>"""

        # Workaround: h1:first-of-type {{ page-break-before: avoid; }} doesn't work
        template = template.replace("<h1>", '<h1 style="page-break-before: avoid;">', 1)
        
        return template

    @staticmethod
    def replace_leading_spaces_in_codehilite(html: str) -> str:
        def repl(match):
            code_block = match.group(1)
            def replace_spaces_in_text(text):
                return re.sub(r"^([ ]+)", lambda m: "&nbsp;" * len(m.group(1)), text, flags=re.MULTILINE)
            parts = re.split(r"(<[^>]+>)", code_block)
            parts = [replace_spaces_in_text(part) if not part.startswith("<") else part for part in parts]
            return f'<div class="codehilite">{"".join(parts)}</div>'

        return re.sub(r'<div class="codehilite">(.*?)</div>', repl, html, flags=re.DOTALL)
