from xhtml2pdf import pisa

class PdfConverter:
    def convert(self, html: str, output_file: str) -> bool:
        with open(output_file, "wb") as pdf_output_file:
            pisa_status = pisa.CreatePDF(
                html,
                dest=pdf_output_file,
                encoding="UTF-8"
            )
        return pisa_status.err == 0
