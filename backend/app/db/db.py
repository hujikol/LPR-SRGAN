import datetime
import databases
from sqlalchemy import Column, Integer, String, Numeric, ForeignKey, orm, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URL = "sqlite:///./lpr_db.db"

database = databases.Database(DATABASE_URL)
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
Base = declarative_base()

class ImgInput(Base):
    __tablename__ = "tbl_img_input"
    id = Column(Integer, primary_key=True)
    img_path = Column(String(255))
    bounding_boxes = orm.relationship("BoundingBox", backref="tbl_img_input")
    tbl_history = orm.relationship("History", back_populates="tbl_img_input", uselist=False)

class BoundingBox(Base):
    __tablename__ = "tbl_bounding_box"
    id = Column(Integer, primary_key=True)
    img_input_id = Column(Integer, ForeignKey("tbl_img_input.id"))
    yolo_confidence = Column(Numeric)
    center_x = Column(Numeric)
    center_y = Column(Numeric)
    width = Column(Numeric)
    height = Column(Numeric)

class CroppedImg(Base):
    __tablename__ = "tbl_cropped_img"
    id = Column(Integer, primary_key=True)
    img_path = Column(String(255))
    tbl_history = orm.relationship("History", back_populates="tbl_cropped_img", uselist=False)

class SuperImg(Base):
    __tablename__ = "tbl_super_img"
    id = Column(Integer, primary_key=True)
    img_path = Column(String(255))
    tbl_history = orm.relationship("History", back_populates="tbl_super_img", uselist=False)

class History(Base):
    __tablename__ = "tbl_history"
    id = Column(Integer, primary_key=True)
    img_input_id = Column(Integer, ForeignKey("tbl_img_input.id"))    
    cropped_img_id = Column(Integer, ForeignKey("tbl_cropped_img.id"))
    super_img_id = Column(Integer, ForeignKey("tbl_super_img.id"))

    tbl_img_input = orm.relationship("ImgInput", back_populates="tbl_history")
    tbl_cropped_img = orm.relationship("CroppedImg", back_populates="tbl_history")
    tbl_super_img = orm.relationship("SuperImg", back_populates="tbl_history")

    date_time = Column(DateTime, default=datetime.datetime.utcnow)
    cropped_text = Column(String(255))
    super_text = Column(String(255))

Base.metadata.create_all(engine)