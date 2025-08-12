from langchain.vectorstores import Chroma
from langchain.schema.retriever import BaseRetriever

from src.config import RETRIEVER_SEARCH_K, RETRIEVER_SCORE_THRESHOLD

# Tạo retriever từ vector database
def create_retriever(vectordb: Chroma) -> BaseRetriever:
    retriever = vectordb.as_retriever(
        search_type="similarity_score_threshold",
        search_kwargs={
            "k": RETRIEVER_SEARCH_K,
            "score_threshold": RETRIEVER_SCORE_THRESHOLD
        }
    )
    print(f"✅ Retriever đã khởi tạo với k={RETRIEVER_SEARCH_K}, threshold={RETRIEVER_SCORE_THRESHOLD}")
    return retriever