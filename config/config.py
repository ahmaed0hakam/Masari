import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'
    SECRET_KEY = 'My|!w>YD/IT[&iE}?yV#>;}Xf]^7YgLV'
    UPLOAD_FOLDER = 'CVs'
    ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx'} 