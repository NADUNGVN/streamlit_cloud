import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Thư mục gốc của dự án (tự động lấy đúng path trên Cloud và local)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # src/
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, ".."))  # gốc repo

# Đường dẫn thư mục chứa PDF gốc
PDF_RAW_DIR = os.path.join(PROJECT_ROOT, "data", "raw_pdfs")
os.makedirs(PDF_RAW_DIR, exist_ok=True)  # tạo nếu chưa có

# Đường dẫn thư mục lưu trữ vector database
VECTOR_DB_DIR = os.path.join(PROJECT_ROOT, "data", "processed_data", "chroma_db")
os.makedirs(VECTOR_DB_DIR, exist_ok=True)

# Đường dẫn tệp ghi log (trong repo hoặc có thể đưa vào /tmp khi Cloud)
LOG_FILE_PATH = os.path.join(PROJECT_ROOT, "logs", "chat_logs.xlsx")

# HuggingFace Embedding Model
EMBEDDING_MODEL_NAME = "dangvantuan/vietnamese-document-embedding"
EMBEDDING_MODEL_KWARGS = {"trust_remote_code": True}

# Groq API & LLM Config
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
LLM_MODEL_NAME = "llama-3.3-70b-versatile"
LLM_TEMPERATURE = 0.5
LLM_MAX_TOKENS = 2000

# Retriever settings
RETRIEVER_SEARCH_K = 5
RETRIEVER_SCORE_THRESHOLD = 0.4
