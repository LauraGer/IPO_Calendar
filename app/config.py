import os
#helps while developing and loads the .env
from dotenv import load_dotenv
from pydantic import BaseModel


load_dotenv()
#load environment variables
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
HOST = os.getenv("HOST")
DATABASE = os.getenv("APP_DB")
USER = os.getenv("POSTGRES_USER")
PASSWORD = os.getenv("POSTGRES_PASSWORD")


base_dir = os.path.dirname(os.path.abspath(__file__))

font_dir = os.path.join(base_dir,"fonts")
default_font = "Urbanist-Bold.ttf"
font_path = os.path.join(font_dir,default_font)

static_path = os.path.join(base_dir, "static")


def sqlalchemy_to_pydantic(sqlalchemy_model):
    fields = {}
    for column in sqlalchemy_model.__table__.columns:
        fields[column.name] = (str)

    return type(
        f'{sqlalchemy_model.__name__}Pydantic',
        (BaseModel,),
        {'__annotations__': fields}
    )