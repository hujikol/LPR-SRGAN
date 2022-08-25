import databases
import sqlalchemy

DATABASE_URL = "sqlite:///./lpr_db.db"

database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

# DEFINE YOUR SCHEMA
# tbl_img_input
tbl_img_input = sqlalchemy.Table(
    "tbl_img_input",
    metadata,
    sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column('img_path', sqlalchemy.String)
)

# tbl_bounding_box
tbl_bounding_box = sqlalchemy.Table(
    "tbl_bounding_box",
    metadata,
    sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column('img_input', sqlalchemy.Integer, sqlalchemy.ForeignKey("tbl_img_input.id")),
    sqlalchemy.Column('yolo_confidence', sqlalchemy.Numeric),
    sqlalchemy.Column('center_x', sqlalchemy.Numeric),
    sqlalchemy.Column('center_y', sqlalchemy.Numeric),
    sqlalchemy.Column('width', sqlalchemy.Numeric),
    sqlalchemy.Column('height', sqlalchemy.Numeric),
)

# tbl_cropped_img
tbl_cropped_img = sqlalchemy.Table(
    "tbl_cropped_img",
    metadata,
    sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column('img_path', sqlalchemy.String)
)

# tbl_super_img
tbl_super_img = sqlalchemy.Table(
    "tbl_super_img",
    metadata,
    sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column('img_path', sqlalchemy.String)
)

#tbl_history
tbl_history = sqlalchemy.Table(
    "tbl_history",
    metadata,
    sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column('img_input', sqlalchemy.Integer, sqlalchemy.ForeignKey("tbl_img_input.id")),
    sqlalchemy.Column('cropped_img', sqlalchemy.Integer, sqlalchemy.ForeignKey("tbl_cropped_img.id")),
    sqlalchemy.Column('super_img', sqlalchemy.Integer, sqlalchemy.ForeignKey("tbl_super_img.id")),
    sqlalchemy.Column('date_time', sqlalchemy.Time),
    sqlalchemy.Column('cropped_text', sqlalchemy.String),
    sqlalchemy.Column('super_text', sqlalchemy.String)
)

engine = sqlalchemy.create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
metadata.create_all(engine)