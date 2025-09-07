import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from config import Config

engine = create_engine(
    f"postgresql+psycopg://{Config.DB_USER}:{Config.DB_PASSWORD}@{Config.DB_HOST}:{Config.DB_PORT}/{Config.DB_NAME}",
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10,
)

ALLOWED_TABLES = {
    "probabilidad_compra",
    "conversion_categorias",
    "brand_group_summary",
    "top5_reconocidas",
    "patrones_temporales",
    "perfil_clientes",
    "sensibilidad_precio",
}

def load_table(table_name: str) -> pd.DataFrame:
    """Load allowed table from RDS"""
    if table_name not in ALLOWED_TABLES:
        raise ValueError(f"Table {table_name} not allowed")
    try:
        query = text(f"SELECT * FROM {table_name}")
        return pd.read_sql(query, engine)
    except SQLAlchemyError as e:
        raise RuntimeError(f"DB error: {e}")
