from sqlalchemy import create_engine
from llama_index.vector_stores.postgres import PGVectorStore
from config.settings import (
    CONNECTION_STRING,
    DB_USER,
    DB_PASS,
    DB_HOST,
    DB_PORT,
    DB_NAME,
    VECTOR_TABLE,
    EMBED_DIM
)

# SQLAlchemy engine - Use CONNECTION_STRING if available
if CONNECTION_STRING:
    engine = create_engine(CONNECTION_STRING, pool_pre_ping=True, pool_size=5, max_overflow=10)
else:
    engine = create_engine(
        f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}",
        pool_pre_ping=True
    )

# PGVectorStore - Use connection pooling parameters
def get_vector_store():
    return PGVectorStore.from_params(
        database=DB_NAME,
        host=DB_HOST,
        port=int(DB_PORT),
        user=DB_USER,
        password=DB_PASS,
        table_name=VECTOR_TABLE,
        embed_dim=EMBED_DIM,
    )
