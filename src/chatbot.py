import os
import asyncio
import nest_asyncio
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain.vectorstores import Chroma
from langchain.schema.retriever import BaseRetriever

from src.config import (
    GROQ_API_KEY, 
    LLM_MODEL_NAME, 
    LLM_TEMPERATURE, 
    LLM_MAX_TOKENS
)

# Định nghĩa Prompt Template
DEFAULT_PROMPT_TEMPLATE = PromptTemplate(
    input_variables=["context", "question"],
    template="""Dựa vào thông tin dưới đây, hãy trả lời câu hỏi bằng tiếng Việt một cách rõ ràng, ngắn gọn.

Thông tin tham khảo:
{context}

Câu hỏi: {question}

Trả lời:"""
)

# Khởi tạo Groq LLM
def create_llm():
    return ChatGroq(
        model_name=LLM_MODEL_NAME,
        temperature=LLM_TEMPERATURE,
        groq_api_key=GROQ_API_KEY,
        max_tokens=LLM_MAX_TOKENS
    )

# Khởi tạo chatbot RAG
def build_chatbot(vectordb: Chroma) -> ConversationalRetrievalChain:
    nest_asyncio.apply()
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    llm = create_llm()

    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True,
        input_key="question",
        output_key="answer"
    )

    retriever = vectordb.as_retriever(
        search_type="similarity_score_threshold",
        search_kwargs={"k": 5, "score_threshold": 0.4}
    )

    qa_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        memory=memory,
        return_source_documents=True,
        combine_docs_chain_kwargs={"prompt": DEFAULT_PROMPT_TEMPLATE},
        verbose=True
    )
    return qa_chain

# Xử lý một truy vấn từ người dùng
def handle_query(question: str, qa_chain: ConversationalRetrievalChain, retriever: BaseRetriever):
    docs = retriever.get_relevant_documents(question)

    if not docs:
        return {
            "answer": "Tôi không tìm thấy thông tin về vấn đề này.",
            "source_documents": []
        }

    result = qa_chain({
        "question": question,
        "chat_history": []
    })
    return result