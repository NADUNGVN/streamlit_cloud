import sys
try:
    import pysqlite3
    sys.modules["sqlite3"] = pysqlite3
    sys.modules["sqlite3"].dbapi2 = pysqlite3
except ImportError:
    pass

import gc, chromadb
from chromadb.config import Settings
from src.config import VECTOR_DB_DIR

def get_client():
    return chromadb.PersistentClient(
        path=VECTOR_DB_DIR,
        settings=Settings(allow_reset=True, anonymized_telemetry=False)
    )

def dispose(vectordb):
    try:
        vectordb._client.reset()          # xoá collection
        vectordb._client._system.stop()   # đóng DuckDB
    except Exception as e:
        print("⚠️ dispose:", e)
    finally:
        vectordb = None
        gc.collect()