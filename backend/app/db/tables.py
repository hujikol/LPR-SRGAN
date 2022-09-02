from sqlalchemy import table, column

tbl_img_input = table(
    "tbl_img_input",
    column("id"),
    column("img_path")
)

tbl_bounding_box = table(
    "tbl_bounding_box",
    column("id"),
    column("img_input"),
    column("yolo_confidence"),
    column("center_x"),
    column("center_y"),
    column("width"),
    column("height")
)

tbl_cropped_img = table(
    "tbl_cropped_img",
    column("id"),
    column("img_path")
)

tbl_super_img = table(
    "tbl_super_img",
    column("id"),
    column("img_path")
)

tbl_history = table(
    "tbl_history",
    column("id"),
    column("img_input"),
    column("cropped_img"),
    column("super_img"),
    column("date_time"),
    column("cropped_text"),
    column("super_text")
)