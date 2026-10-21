import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app

# Çíä Ïæ ÊÇ get_db ÈÇ åã İÑŞ ÏÇÑäÏ æ åÑ Ïæ ÈÇíÏ override ÔæäÏ
import app.database as db_mod
import app.core.database as core_db_mod

TEST_DB_URL = "sqlite:///./test_nexustask.db"

engine = create_engine(
    TEST_DB_URL,
    connect_args={"check_same_thread": False},
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="session", autouse=True)
def create_tables_once():
    # ÇÑ Base åÇ ÌÏÇ ÈÇÔäÏ ÈÇíÏ åÑ Ïæ ÑÇ create_all ˜äí.
    # æáí ãÚãæáÇ í˜í åÓÊäÏ ÈÇ Çíä ÍÇá ÇãäÊÑ Çíä ÇÓÊ ˜å åÑ Ïæ ÑÇ ÕÏÇ ÈÒäíã.
    db_mod.Base.metadata.drop_all(bind=engine)
    db_mod.Base.metadata.create_all(bind=engine)

    # ÇÑ app.core.database åã Base ÌÏÇ ÏÇÑÏ (Çåí) Çíä åã ÇÖÇİå ãíÔæÏ:
    if hasattr(core_db_mod, "Base"):
        core_db_mod.Base.metadata.drop_all(bind=engine)
        core_db_mod.Base.metadata.create_all(bind=engine)

    yield

    db_mod.Base.metadata.drop_all(bind=engine)
    if hasattr(core_db_mod, "Base"):
        core_db_mod.Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def client():
    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    # override åÑ Ïæ ãÓíÑ
    app.dependency_overrides[db_mod.get_db] = override_get_db
    app.dependency_overrides[core_db_mod.get_db] = override_get_db

    with TestClient(app) as c:
        yield c

    app.dependency_overrides.clear()
