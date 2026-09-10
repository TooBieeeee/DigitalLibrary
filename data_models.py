from datetime import date
from typing import List, Optional
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()


class Author(db.Model):
    __tablename__ = "author"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    birth_date: Mapped[date] = mapped_column(nullable=False)
    date_of_death: Mapped[Optional[date]] = mapped_column(default=None)

    books: Mapped[List["Book"]] = relationship(back_populates="author")

    def __repr__(self) -> str:
        return f"Author{self.id}(Name: {self.name}, Birthday: {self.birth_date}, Date of Death: {self.date_of_death})"


class Book(db.Model):
    __tablename__ = "book"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    isbn: Mapped[str] = mapped_column(String, nullable=False)
    title: Mapped[str] = mapped_column(String, nullable=False)
    author_id: Mapped[int] = mapped_column(ForeignKey("author.id"), nullable=False)
    publication_year: Mapped[int] = mapped_column(nullable=False)

    author: Mapped["Author"] = relationship(back_populates="books")

    def __repr__(self) -> str:
        return f"Book{self.id}(ISBN: {self.isbn}, Title: {self.title}, Author: {self.author_id}, Publication Year: {self.publication_year})"