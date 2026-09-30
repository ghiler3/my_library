from fastapi import APIRouter, status, HTTPException, Response

from database import SessionDep
from repository import BookRepository
from schemas.books import SBookAdd, SBook

router = APIRouter(prefix="/books", tags=["Книги"])


@router.post("", response_model=SBook, status_code=status.HTTP_201_CREATED)
async def post_book(book: SBookAdd, session: SessionDep):

    book_model = await BookRepository.add_book(book, session)

    return book_model


@router.get("", response_model=list[SBook], status_code=status.HTTP_200_OK)
async def get_books(session: SessionDep):

    result = await BookRepository.find_all(session)

    return result


@router.get("/{book_id}", response_model=SBook, status_code=status.HTTP_200_OK)
async def get_book(book_id: int, session: SessionDep):

    result = await BookRepository.find_one(book_id, session)

    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Книга не найдена"
        )

    return result


@router.put("/{book_id}", response_model=SBook, status_code=status.HTTP_200_OK)
async def upd_book(book_id: int, book: SBookAdd, session: SessionDep):
    result = await BookRepository.update_book(book_id, book, session)

    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Книга не найдена"
        )

    return result


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def del_book(book_id: int, session: SessionDep):
    result = await BookRepository.delete_book(book_id, session)

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Книга не найдена"
        )

    return Response(status_code=status.HTTP_204_NO_CONTENT)
