from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.models import User
from src.auth.schemas import CreateUserModel
from .util import generate_password_hash

class UserService:
    async def get_user(self, email:str , sesssion : AsyncSession):
        statement = select(User).where(User.email == email)

        result = await sesssion.exec(statement)
        if result is None:
            return None
        
        user = result.first()
        return user
    
    async def create_user(self, request: CreateUserModel, session: AsyncSession):
        create_user_dict = request.model_dump()

        new_user = User(**create_user_dict)
        new_user.password_hash = generate_password_hash(create_user_dict["password"])
        session.add(new_user)
        await session.commit()

        return new_user