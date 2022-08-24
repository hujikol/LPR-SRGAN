from pydantic import BaseModel

class ImageIn(BaseModel):
    id: int
    img_path: str

class Image(BaseModel):
    img_path: str