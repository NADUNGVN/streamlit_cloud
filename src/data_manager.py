import os
import shutil
from typing import List
from src.config import PDF_RAW_DIR

# Lấy danh sách tất cả file PDF đã tải lên
def list_pdf_files() -> List[str]:
    return [f for f in os.listdir(PDF_RAW_DIR) if f.lower().endswith(".pdf")]

# Thêm file PDF mới (ghi đè nếu trùng tên)
def save_uploaded_pdf(file_name: str, file_data: bytes) -> str:
    os.makedirs(PDF_RAW_DIR, exist_ok=True)
    file_path = os.path.join(PDF_RAW_DIR, file_name)
    with open(file_path, "wb") as f:
        f.write(file_data)
    return file_path

# Xóa một file PDF
def delete_pdf_file(file_name: str) -> bool:
    file_path = os.path.join(PDF_RAW_DIR, file_name)
    if os.path.exists(file_path):
        os.remove(file_path)
        return True
    return False

# Xóa toàn bộ PDF (hữu ích khi tái tạo vector database)
def clear_all_pdfs():
    if os.path.exists(PDF_RAW_DIR):
        shutil.rmtree(PDF_RAW_DIR)
    os.makedirs(PDF_RAW_DIR, exist_ok=True)