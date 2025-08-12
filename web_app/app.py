import os
import streamlit as st
from datetime import datetime
import time
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.config import PDF_RAW_DIR
from src.data_manager import list_pdf_files, save_uploaded_pdf, delete_pdf_file
from src.embeddings_manager import rebuild_vector_db, load_vector_database
from src.retrieval import create_retriever
from src.chatbot import build_chatbot, handle_query
from src.logging_manager import log_interaction

st.set_page_config(
    page_title="RAG Chatbot Hành Chính Công",
    page_icon="🤖",
    layout="wide"
)

# Khởi tạo trạng thái
if "messages" not in st.session_state:
    st.session_state.messages = []

if "chatbot" not in st.session_state:
    try:
        vectordb = load_vector_database()
        retriever = create_retriever(vectordb)
        chatbot = build_chatbot(vectordb)
        st.session_state.chatbot = chatbot
        st.session_state.retriever = retriever
        st.session_state.messages = []
        st.toast("✅ Chatbot đã sẵn sàng!", icon="🎉")
    except Exception as e:
        st.error(f"❌ Lỗi khi khởi tạo chatbot: {e}")

# Sidebar
with st.sidebar:
    st.title("⚙️ Quản lý dữ liệu")

    # Upload
    st.subheader("📤 Tải lên PDF")
    uploaded_files = st.file_uploader("Chọn file PDF", type=["pdf"], accept_multiple_files=True)
    if uploaded_files:
        for file in uploaded_files:
            save_uploaded_pdf(file.name, file.getbuffer())
            st.success(f"Đã lưu: {file.name}")
        st.warning("⚠️ Hãy nhấn nút 'Tạo lại Vector DB' để cập nhật dữ liệu.")

    # Xem danh sách
    st.subheader("📂 Tài liệu hiện có")
    pdfs = list_pdf_files()
    if pdfs:
        for file in pdfs:
            col1, col2 = st.columns([4, 1])
            col1.markdown(f"- {file}")
            if col2.button("❌", key=f"del_{file}"):
                delete_pdf_file(file)
                st.rerun()
    else:
        st.info("Không có tài liệu nào.")

        # Xây dựng lại vector DB
    if st.button("🔄 Tạo lại Vector DB"):
        from src.chroma_utils import dispose            

        with st.spinner("Đang tái tạo..."):
            # 1. Giải phóng DB cũ (nếu đang mở)
            if "vectordb" in st.session_state:
                dispose(st.session_state.vectordb)
                st.session_state.pop("vectordb", None)
                st.session_state.pop("retriever", None)
                st.session_state.pop("chatbot", None)

            # 2. Xoá thư mục & tạo DB mới
            vectordb = rebuild_vector_db()

            # 3. Nạp retriever + chatbot mới
            st.session_state.vectordb  = vectordb
            st.session_state.retriever = create_retriever(vectordb)
            st.session_state.chatbot   = build_chatbot(vectordb)

        st.toast("✅ Vector DB đã được tái tạo!", icon="🎉")
        st.rerun() 

# Header
st.title("💬 RAG Chatbot Hành Chính Công")

# Vùng hiển thị tin nhắn
for msg in st.session_state.messages:
    role = msg["role"]
    content = msg["content"]
    time_str = msg["timestamp"]
    if role == "user":
        st.markdown(f"**👤 Bạn** [{time_str}]: {content}")
    else:
        st.markdown(f"**🤖 Bot** [{time_str}]: {content}")
        if msg.get("sources"):
            with st.expander("📚 Nguồn tham khảo"):
                for i, doc in enumerate(msg["sources"]):
                    source = os.path.basename(doc.metadata.get("source", "Không rõ"))
                    page = doc.metadata.get("page", "N/A")
                    preview = doc.page_content[:200]
                    st.markdown(f"**{i+1}.** *{source}* (trang {page})\n\n{preview}...")

# Chat input
query = st.chat_input("Nhập câu hỏi về thủ tục hành chính...")
if query and "chatbot" in st.session_state:
    chatbot = st.session_state.chatbot
    retriever = st.session_state.retriever

    st.session_state.messages.append({
        "role": "user",
        "content": query,
        "timestamp": datetime.now().strftime("%H:%M:%S")
    })

    with st.spinner("Đang xử lý..."):
        result = handle_query(query, chatbot, retriever)

    st.session_state.messages.append({
        "role": "assistant",
        "content": result["answer"],
        "sources": result.get("source_documents", []),
        "timestamp": datetime.now().strftime("%H:%M:%S")
    })

    # Ghi log
    log_interaction(
        context="Hành chính công",
        question=query,
        assistant_thought="Truy xuất từ RAG",
        answer=result["answer"],
        references=result.get("source_documents", [])
    )

    st.rerun()