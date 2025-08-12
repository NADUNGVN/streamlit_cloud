import os
import pandas as pd
from datetime import datetime
from src.config import LOG_FILE_PATH

# Ghi log vào file Excel
def log_interaction(context: str, question: str, assistant_thought: str, answer: str, references: list):
    os.makedirs(os.path.dirname(LOG_FILE_PATH), exist_ok=True)
    timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    ref_texts = []
    for doc in references:
        source = doc.metadata.get("source", "Không rõ")
        page = doc.metadata.get("page", "Không rõ")
        content = doc.page_content[:200].replace("\n", " ").strip()
        ref_texts.append(f"[{os.path.basename(source)} - Trang {page}]: {content}...")

    data = {
        "Timestamp": [timestamp],
        "Context": [context],
        "Question": [question],
        "Assistant_Thought": [assistant_thought],
        "Answer": [answer],
        "References": ["\n".join(ref_texts)]
    }

    new_df = pd.DataFrame(data)

    if os.path.exists(LOG_FILE_PATH):
        existing_df = pd.read_excel(LOG_FILE_PATH)
        updated_df = pd.concat([existing_df, new_df], ignore_index=True)
    else:
        updated_df = new_df

    updated_df.to_excel(LOG_FILE_PATH, index=False)
    print("✅ Ghi log thành công.")