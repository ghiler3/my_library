from sqlalchemy.ext.asyncio import AsyncSession

from models.books import BooksModel
from schemas.books import SBookAdd
from sqlalchemy import select, delete


class BookRepository:
    @classmethod
    async def add_book(cls, data: SBookAdd, session: AsyncSession) -> BooksModel:
        data_dict = data.model_dump()

        book = BooksModel(**data_dict)

        session.add(book)
        await session.commit()
        await session.refresh(book)

        return book

    @classmethod
    async def find_all(cls, session: AsyncSession) -> list[BooksModel]:
        query = select(BooksModel)

        result = await session.execute(query)

        books_models = result.scalars().all()
        return list(books_models)

    @classmethod
    async def find_one(cls, book_id: int, session: AsyncSession) -> BooksModel | None:
        query = select(BooksModel).where(BooksModel.id == book_id)
        result = await session.execute(query)

        return result.scalar_one_or_none()

    @classmethod
    async def update_book(
        cls, book_id: int, data: SBookAdd, session: AsyncSession
    ) -> BooksModel | None:
        book = await cls.find_one(book_id, session)

        if book is None:
            return None

        for field, value in data.model_dump().items():
            setattr(book, field, value)

        await session.commit()
        await session.refresh(book)

        return book

    @classmethod
    async def delete_book(cls, book_id: int, session: AsyncSession) -> bool:
        book = await cls.find_one(book_id, session)

        if book is None:
            return False

        await session.delete(book)
        await session.commit()

        return True
