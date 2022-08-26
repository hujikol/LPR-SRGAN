from sqlalchemy import table, column

tbl_img_input = table(
    "tbl_img_input",
    column("id"),
    column("img_path")
)