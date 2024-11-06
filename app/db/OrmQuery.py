from sqlalchemy import select, and_
from fastapi import Depends

from app.core.security import get_user_by_token
from app.db.database import engine, Base, session_factory
from app.db.dbstruct import UserOrm, TaskOrm
from app.api.models.task import TaskCreate, TaskUpdate

class OrmQuery:
    @staticmethod
    def create_tables():
        Base.metadata.create_all(engine)
    
    @staticmethod
    def insert_data(username: str, email: str, hashed_password: str):
        with session_factory() as session:
            new_user = UserOrm(
                username=username, 
                email=email, 
                hashed_password=hashed_password
            )
            session.add(new_user)
            session.flush()
            session.commit()

    @staticmethod
    def select_users(username: str):
        with session_factory() as session:
            query = select(UserOrm).filter(UserOrm.username==username)
            result = session.execute(query)
            users = result.scalars().all()
            return users
        
    @staticmethod
    def select_access_user(username: str):
        with session_factory() as session:
            query = select(UserOrm).filter(UserOrm.username == username)
            user = session.execute(query).scalars().first()
            return user

    @staticmethod
    def insert_task(task: TaskCreate, owner_id: int):
        with session_factory() as session:
            task_query = TaskOrm(**task.dict(), owner_id=owner_id)
            session.add(task_query)
            session.flush()
            session.commit()
            session.refresh(task_query)

    @staticmethod
    def select_tasks(owner_id: int, skip: int, limit: int):
        with session_factory() as session:
            query = select(TaskOrm).filter(
                TaskOrm.owner_id == owner_id).offset(skip).limit(limit)
            result = session.execute(query).scalars().all()
            return result
        
    @staticmethod
    def select_task_for_id(task_id: int, owner_id: int):
        with session_factory() as session:
            query = select(TaskOrm).filter(
                and_(
                    TaskOrm.id == task_id,
                    TaskOrm.owner_id == owner_id
                )
                )
            result = session.execute(query).scalars().first()
            return result
        
    @staticmethod
    def put_task(task_id: int, task_update: TaskUpdate, owner_id: int):
        with session_factory() as session:
            query = select(TaskOrm).filter(
                and_(
                    TaskOrm.id == task_id, 
                    TaskOrm.owner_id == owner_id
                )
            )
            result = session.execute(query).scalars().first()

            if result is None:
                return None
            
            for key, value in task_update.dict().items():
                setattr(result, key, value)

            session.commit()
            session.refresh(result)
            
            return result

    @staticmethod
    def delete_task(task_id: int, owner_id: int):
        with session_factory() as session:
            query = select(TaskOrm).filter(
                and_(
                    TaskOrm.id == task_id, 
                    TaskOrm.owner_id == owner_id
                )
            ) 
            result = session.execute(query).scalars().first()

            if result is None:
                return None
            
            session.delete(result)
            session.commit()

