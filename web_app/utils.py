import os
from datetime import datetime

# Định dạng giờ phút giây
def format_timestamp():
    return datetime.now().strftime("%H:%M:%S")

# Rút gọn nội dung văn bản
def shorten_text(text: str, max_length: int = 200) -> str:
    text = text.strip().replace("\n", " ")
    return text[:max_length] + "..." if len(text) > max_length else text

# Lấy tên tệp từ metadata tài liệu
def get_doc_filename(doc) -> str:
    return os.path.basename(doc.metadata.get("source", "Không rõ"))

# Lấy trang từ metadata tài liệu
def get_doc_page(doc) -> str:
    return str(doc.metadata.get("page", "N/A"))