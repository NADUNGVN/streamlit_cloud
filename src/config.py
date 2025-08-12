import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Đường dẫn thư mục chứa PDF gốc
PDF_RAW_DIR = r"E:\WORK\project\streamlit_cloud\data\raw_pdfs"

# Đường dẫn thư mục lưu trữ vector database
VECTOR_DB_DIR = r"E:\WORK\project\streamlit_cloud\data\processed_data\chroma_db"

# Đường dẫn tệp ghi log
LOG_FILE_PATH = r"D:\work\rag_chatbot_project\logs\logschat_logs.xlsx"

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