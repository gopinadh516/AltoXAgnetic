import zipfile
import io
import base64

class ExportAgent:
    """
    Packages code for download.
    """
    def run(self, code, filename="generated_code.html"):
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w") as zf:
            zf.writestr(filename, code)
        zip_buffer.seek(0)
        b64 = base64.b64encode(zip_buffer.read()).decode()
        download_link = f"data:application/zip;base64,{b64}"
        return download_link