from softwarecitationauditor import downloader
import os

def test_download_local_file(tmp_path):
    test_file = tmp_path / "test.pdf"
    test_file.write_text("fake pdf content")
    result = downloader.download_pdf(str(test_file))
    assert os.path.exists(result)