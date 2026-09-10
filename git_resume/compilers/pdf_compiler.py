import os
from typing import List

class PdfCompiler:
    """Exports DOCX files to PDF using MS Word COM automation with graceful fallback."""

    def export_all(self, resume_dir: str) -> List[str]:
        paths = [
            os.path.abspath(os.path.join(resume_dir, fname))
            for fname in os.listdir(resume_dir)
            if fname.endswith(".docx") and not fname.startswith("~$")
        ]
        return self.export_files(paths)

    def export_files(self, docx_paths: List[str]) -> List[str]:
        """Exports only the given .docx files to PDF -- used for a scoped sync so a
        commit in one repo doesn't pay the (slow) Word COM export cost for every
        persona resume, only the ones whose text actually changed."""
        exported = []
        if not docx_paths:
            return exported
        try:
            import win32com.client
            word = win32com.client.Dispatch("Word.Application")
            word.Visible = False
            try:
                for docx_path in docx_paths:
                    fname = os.path.basename(docx_path)
                    if not fname.endswith(".docx") or fname.startswith("~$"):
                        continue
                    docx_path = os.path.abspath(docx_path)
                    pdf_path = os.path.splitext(docx_path)[0] + ".pdf"
                    doc = word.Documents.Open(docx_path)
                    doc.SaveAs(pdf_path, FileFormat=17)  # 17 = wdFormatPDF
                    doc.Close()
                    exported.append(pdf_path)
            finally:
                word.Quit()
        except Exception as e:
            print(f"[WARN] PDF export skipped via Word COM: {e}")
        return exported
