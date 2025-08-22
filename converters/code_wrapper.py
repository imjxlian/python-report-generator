import re

class CodeWrapper:
    def __init__(self, font_size_px, available_space_cm, cm_px_ratio, wrap_symbol="> "):
        self.cm_px_ratio = cm_px_ratio
        self.wrap_symbol = wrap_symbol
        self.max_chars = self.calc_max_chars_per_line(font_size_px, available_space_cm)

    def calc_max_chars_per_line(self, font_size_px: int, available_space_cm: int) -> int:
        # Convert cm -> px
        available_px = available_space_cm / (1 / self.cm_px_ratio)
        return round(available_px / font_size_px)

    def wrap_code_lines(self, code_text: str) -> str:
        lines = code_text.split("\n")
        wrapped_lines = []

        for line in lines:
            first_line = True

            # Keep wrapping while the line is too long
            while len(line) > self.max_chars:
                # For the first chunk use full max_chars.
                # For subsequent chunks, leave room for the wrap symbol.
                effective_max = self.max_chars if first_line else self.max_chars - len(self.wrap_symbol)
                
                # Try to cut at the last space before the limit
                split_point = line.rfind(" ", 0, effective_max)

                # If not possible, break-word
                if split_point == -1:
                    split_point = effective_max

                # Append to the wrapped lines
                if first_line:
                    wrapped_lines.append(line[:split_point])
                else:
                    wrapped_lines.append(self.wrap_symbol + line[:split_point])

                # Remove white spaces on the left
                line = line[split_point:].lstrip()
                first_line = False

            # Append the final remaining part of the line
            if not first_line:
                wrapped_lines.append(self.wrap_symbol + line)
            else:
                wrapped_lines.append(line)

        return "\n".join(wrapped_lines)

    def wrap_code_blocks(self, md_text: str) -> str:
        def repl(match):
            # Extract the language and code from the markdown code block
            lang = match.group(1) or ""
            code = match.group(2)

            # Wrap lines
            wrapped = self.wrap_code_lines(code)
            return f"```{lang}\n{wrapped}\n```"

        # Regex to find all Markdown code blocks and apply the replacement function
        # - ```(\w*)\n captures the optional language specifier
        # - (.*?)``` captures everything inside the code block (non-greedy)
        # - flags=re.DOTALL makes . match newlines so the code block can be multiline
        # Note: I used AI to generate this regex (GPT 4)
        return re.sub(r"```(\w*)\n(.*?)```", repl, md_text, flags=re.DOTALL)
