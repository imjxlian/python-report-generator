import markdown

class MarkdownConverter:
    def __init__(self):
        self.md = markdown.Markdown(extensions=['abbr', 'tables', 'fenced_code', 'codehilite', 'nl2br', 'sane_lists'])

    def convert_file(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()
        return self.md.convert(text)

    def convert_text(self, markdown_text):
        return self.md.convert(markdown_text)

