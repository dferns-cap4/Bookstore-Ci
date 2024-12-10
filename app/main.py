from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database import get_db, init_db
from app.models import Book
from app.schemas import BookCreate, BookResponse
from app.database import engine

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    """
    Ensure the database is initialized on startup.
    """
    await init_db(reset=True)

@app.on_event("shutdown")
async def on_shutdown():
    """
    Dispose of the database engine on shutdown to close all connections.
    """
    await engine.dispose()

@app.post("/books/", response_model=BookResponse, status_code=201)
async def create_book(book: BookCreate, db: AsyncSession = Depends(get_db)):
    """
    Create a new book record.
    """
    new_book = Book(**book.model_dump())
    try:
        db.add(new_book)
        await db.commit()
        await db.refresh(new_book)
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
    return new_book

@app.get("/books/", response_model=list[BookResponse])
async def get_books(db: AsyncSession = Depends(get_db)):
    """
    Retrieve a list of all books.
    """
    result = await db.execute(select(Book))
    books = result.scalars().all()
    return books
