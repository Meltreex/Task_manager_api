from typing import List, Set
from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect

from app.api.models.task import TaskCreate, TaskUpdate, TaskResponse
from app.core.security import get_user_by_token
from app.db.database import session_factory
from app.db.dbstruct import TaskOrm, UserOrm
from app.db.OrmQuery import OrmQuery

router = APIRouter()

active_connections: Set[WebSocket] = set()


@router.websocket("/ws/tasks/{client_id}")
async def websocket_endpoint(client_id: int, websocket: WebSocket):
    await websocket.accept()
    active_connections.add(websocket)
    try:
        while True:
            message = await websocket.receive_text()
            for connection in active_connections:
                await connection.send_text(f"Client with {client_id} wrote {message}!")
    except WebSocketDisconnect:
        active_connections.remove(websocket)


@router.post("/tasks/")
def create_task(task: TaskCreate, username: str = Depends(get_user_by_token)):

    user = OrmQuery.select_access_user(username=username)

    task_db = OrmQuery.insert_task(task=task, owner_id=user.id)
    for connection in active_connections:
        connection.send_text(f"New task created")
    return {"message": "A new task has been added"} 


@router.get("/tasks/", response_model=List[TaskResponse])
def read_tasks(skip: int = 0, limit: int = 10, username: str = Depends(get_user_by_token)):
    user = OrmQuery.select_access_user(username=username)

    tasks = OrmQuery.select_tasks(owner_id=user.id, skip=skip, limit=limit)
    return tasks


@router.get("/tasks/{task_id}", response_model=TaskResponse)
def read_task(task_id: int, username: str = Depends(get_user_by_token)):
    user = OrmQuery.select_access_user(username=username)

    task_id = OrmQuery.select_task_for_id(task_id, user.id)
    if task_id is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task_id


@router.put("/tasks/{task_id}")
def update_task(task_id: int, task_update: TaskUpdate, username: str = Depends(get_user_by_token)):

    user = OrmQuery.select_access_user(username=username)

    task_id = OrmQuery.put_task(task_id, task_update, user.id)

    if task_id is None:
        raise HTTPException(status_code=404, detail="Task not found")
    
    for connection in active_connections:
        connection.send_text(f"Task {task_id.id} updated")
    return {"message": "A task has been updated"} 


@router.delete("/tasks/{task_id}")
def delete_task(task_id: int, username: str = Depends(get_user_by_token)):

    user = OrmQuery.select_access_user(username=username)

    response = OrmQuery.select_task_for_id(task_id, user.id)

    if response is None:
        raise HTTPException(status_code=404, detail="Task not found")
    
    
    for connection in active_connections:
        connection.send_text(f"Task {response.id} deleted")

    OrmQuery.delete_task(task_id, user.id)

    return {"message": "A task has been deleted"} 