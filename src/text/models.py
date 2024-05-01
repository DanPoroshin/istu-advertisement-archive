from datetime import datetime

from sqlalchemy import Column, Integer, String, MetaData, Table, TIMESTAMP, ARRAY

from src.db import Base

metadata = MetaData()

text = Table(
    "text",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("title", String),
    Column("text", String),
    Column("kirillic_text", String),
    Column("lemmatized_text", ARRAY(String)),
    Column("image", String),
    Column("comment", String),
    Column("created_at", TIMESTAMP, default=datetime.now),
)


class Text(Base):
    __tablename__ = "text"
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)
    text = Column(String)
    kirillic_text = Column(String)
    lemmatized_text = Column(ARRAY(String))
    image = Column(String)
    comment = Column(String)
    created_at = Column(TIMESTAMP, default=datetime.now)
