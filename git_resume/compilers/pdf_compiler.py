import os
from typing import List

class PdfCompiler:
    """Exports DOCX files to PDF using MS Word COM automation with graceful fallback."""

    def export_all(self, resume_dir: str) -> List[str]:
        exported = []
        try:
            import win32com.client
            word = win32com.client.Dispatch("Word.Application")
            word.Visible = False
            try:
                for fname in os.listdir(resume_dir):
                    if fname.endswith(".docx") and not fname.startswith("~$"):
                        docx_path = os.path.abspath(os.path.join(resume_dir, fname))
                        pdf_path = os.path.splitext(docx_path)[0] + ".pdf"
                        doc = word.Documents.Open(docx_path)
                        doc.SaveAs(pdf_path, FileFormat=17) # 17 = wdFormatPDF
                        doc.Close()
                        exported.append(pdf_path)
            finally:
                word.Quit()
        except Exception as e:
            print(f"[WARN] PDF export skipped via Word COM: {e}")
        return exported
