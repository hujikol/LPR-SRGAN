import databases
import sqlalchemy

DATABASE_URL = "sqlite:///./lpr_db.db"

database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

# DEFINE YOUR SCHEMA
tbl_img_input = sqlalchemy.Table(
    "tbl_img_input",
    metadata,
    sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column('img_path', sqlalchemy.String)
)

engine = sqlalchemy.create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
metadata.create_all(engine)