from sqlalchemy import create_engine
from llama_index.vector_stores.postgres import PGVectorStore
from config.settings import DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_NAME, VECTOR_TABLE, EMBED_DIM

# SQLAlchemy engine
engine = create_engine(
    f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

# PGVectorStore
vector_store = PGVectorStore.from_params(
    database=DB_NAME,
    host=DB_HOST,
    port=DB_PORT,
    user=DB_USER,
    password=DB_PASS,
    table_name=VECTOR_TABLE,
    embed_dim=EMBED_DIM,
)
