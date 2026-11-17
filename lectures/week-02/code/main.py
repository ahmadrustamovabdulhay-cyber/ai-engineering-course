import os
from collections.abc import Iterator
from datetime import date
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Query
from pydantic import BaseModel, ConfigDict
from sqlalchemy import Text, create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column


class Base(DeclarativeBase):
    pass


class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(Text)


class Loan:
    # Homework: turn this into an ORM model for the existing loans table.
    pass


class BookRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str


class LoanRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    book_id: int
    member_id: int
    borrowed_on: date
    returned_on: date | None


engine = create_engine(os.environ["DATABASE_URL"])
app = FastAPI(title="Library SQL Homework")


def get_session() -> Iterator[Session]:
    with Session(engine) as session:
        yield session


@app.get("/books", response_model=list[BookRead])
def list_books(session: Annotated[Session, Depends(get_session)]):
    statement = select(Book).order_by(Book.id)
    return session.scalars(statement).all()


@app.get("/loans", response_model=list[LoanRead])
def list_loans(
    session: Annotated[Session, Depends(get_session)],
    is_open: Annotated[bool | None, Query(alias="open")] = None,
):
    # Homework: select the loans that match is_open and order them by ID.
    raise HTTPException(status_code=501, detail="Complete the loan query for Homework 04")
