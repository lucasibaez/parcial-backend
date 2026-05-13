from sqlmodel import create_engine, Session

# 🔥 conexión a PostgreSQL
DATABASE_URL = "postgresql://postgres:root@localhost:5432/parcial1"

engine = create_engine(
    DATABASE_URL,
    echo=True
)


def get_session():
    with Session(engine) as session:
        yield session