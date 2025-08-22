import markdown
from pygments.formatters import HtmlFormatter

class MarkdownConverter:
    def __init__(self):
        self.pygments_css = HtmlFormatter(style="emacs").get_style_defs(".codehilite")

    def convert(self, md_text: str) -> str:
        return markdown.markdown(
            md_text,
            extensions=["fenced_code", "tables", "codehilite", "attr_list", "nl2br"],
            extension_configs={
                "codehilite": {
                    "linenums": False,
                    "guess_lang": True,
                    "css_class": "codehilite",
                    "use_pygments": True
                }
            }
        )
