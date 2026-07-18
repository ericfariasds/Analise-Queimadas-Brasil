#Bibliotecas
import os
import logging
from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine

#Variáveis de ambiente
_ENV_PATH = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=_ENV_PATH if _ENV_PATH.exists() else None)
 
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME", "db_queimadas")
 
_REQUIRED_VARS = ["DB_USER", "DB_PASSWORD", "DB_HOST", "DB_PORT", "DB_NAME"]

def _validar_env() -> None:
    """Falha cedo e com mensagem clara se o .env não estiver configurado."""
    faltando = [v for v in _REQUIRED_VARS if not os.getenv(v)]
    if faltando:
        raise EnvironmentError(
            f"Variáveis de ambiente ausentes: {', '.join(faltando)}. "
            f"Copie '.env.example' para '.env' e preencha os valores antes de continuar."
        )

#Paths do projeto
BASE_DIR = Path(__file__).resolve().parent
RAW_DATA_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DATA_DIR = BASE_DIR / "data" / "processed"
SQL_DIR = BASE_DIR / "sql"
 
PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)

#Logger padrão
def get_logger(nome: str) -> logging.Logger:
    """Retorna um logger configurado de forma consistente para todo o projeto."""
    logger = logging.getLogger(nome)
    if not logger.handlers:  # evita handlers duplicados se a célula rodar 2x
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
            datefmt="%H:%M:%S",
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
        logger.propagate = False
    return logger

#Engine factory
def get_engine(database: str | None = None) -> Engine:
    """
    Cria uma engine SQLAlchemy para o MySQL.
 
    Parameters
    ----------
    database : str | None
        Nome do banco. Se None, conecta apenas no servidor (útil para
        rodar CREATE DATABASE). Se omitido, usa DB_DATABASE do .env.
 
    Raises
    ------
    EnvironmentError
        Se alguma variável obrigatória do .env estiver faltando.
    """
    _validar_env()
    db_part = database if database is not None else ""
    url = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{db_part}"
    return create_engine(url, pool_pre_ping=True)