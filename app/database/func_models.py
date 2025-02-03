from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.future import select
from .models import User, Base

engine = create_async_engine("postgresql+asyncpg://myuser:mypassword@localhost:5500/postgres")
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

async def get_session():
    async with async_session() as session:
        yield session
        
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        
async def get_user(session, name):        
    query = select(User).where(User.name == name)
    result = await session.execute(query)
    following = result.scalars().first()
    return following