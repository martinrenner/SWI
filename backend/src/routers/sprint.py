from typing import Annotated
from fastapi import APIRouter, Depends
from sqlmodel import Session
from schemas.task import TaskRead
from services.sprint_service import SprintService
from schemas.default import DefaultBase
from schemas.sprint import SprintCreate, SprintRead, SprintReadChart, SprintUpdate
from tokens.access_token import AccessToken
from database import get_session


sprint_router = APIRouter(prefix="/sprint", tags=["Sprint"])

db_dependency = Annotated[Session, Depends(get_session)]
user_dependency = Annotated[dict, Depends(AccessToken.verify_token)]

sprint_service = SprintService()


@sprint_router.post("/", response_model=SprintRead)
def create_sprint(project_id: int, sprint_create: SprintCreate, user: user_dependency, session: db_dependency):
    """
    ## Create a new sprint

    Create a new sprint for a project.

    - **project_id (int)**: The ID of the project.
    - **sprint_create (SprintCreate)**: The data for creating the sprint.

    Returns:
    - `SprintRead`: The created sprint.
    """
    sprint = sprint_service.insert_sprint_db(project_id, sprint_create, user.id, session)
    return SprintRead.from_sprint(sprint)

@sprint_router.get("/{sprint_id}/", response_model=SprintRead)
def read_sprint(sprint_id: int, user: user_dependency, session: db_dependency):
    """
    ## Read a sprint

    Retrieve information about a specific sprint.

    - **sprint_id (int)**: The ID of the sprint.

    Returns:
    - `SprintRead`: The details of the sprint.
    """
    sprint = sprint_service.select_sprint_by_id_db(sprint_id, user.id, session)
    return SprintRead.from_sprint(sprint)

@sprint_router.post("/{sprint_id}/assign-task/", response_model=TaskRead)
def assign_task_to_sprint(sprint_id: int, task_id: int, user: user_dependency, session: db_dependency):
    """
    Assigns a task to a sprint.

    - **sprint_id (int)**: The ID of the sprint to assign the task to.
    - **task_id (int)**: The ID of the task to be assigned.

    Returns:
    - `TaskRead`: The assigned task.

    """
    task = sprint_service.assign_task_to_sprint_db(task_id, sprint_id, user.id, session)
    return TaskRead.from_task(task)

@sprint_router.patch("/{sprint_id}/update/", response_model=SprintRead)
def update_sprint(sprint_id: int, sprint_update: SprintUpdate, user: user_dependency, session: db_dependency):
    """
    ## Update a sprint

    Update a sprint in the database.

    - **sprint_id (int)**: The ID of the sprint.
    - **sprint_update (SprintUpdate)**: The updated sprint data.

    Returns:
    - `SprintRead`: The updated sprint data.
    """
    sprint = sprint_service.update_sprint_db(sprint_id, sprint_update, user.id, session)
    return SprintRead.from_sprint(sprint)

@sprint_router.delete("/{sprint_id}/delete/", response_model=DefaultBase)
def delete_sprint(sprint_id: int, user: user_dependency, session: db_dependency):
    """
    ## Delete a sprint
    
    Delete a sprint from the specified project.

    - **project_id (int)**: The ID of the project.
    - **sprint_id (int)**: The ID of the sprint to be deleted.

    Returns:
    - `DefaultBase`: The response indicating the success of the deletion.
    """
    sprint_service.delete_sprint_db(sprint_id, user.id, session)
    return DefaultBase.from_default(message="Sprint deleted successfully.")

@sprint_router.get("/{sprint_id}/chart/", response_model=SprintReadChart)
def read_sprint_chart(sprint_id: int, user: user_dependency, session: db_dependency):
    """
    ## Read data for a sprint chart

    Retrieve a data for chart for a specific sprint.

    - **sprint_id (int)**: The ID of the sprint.

    Returns:
    - `SprintReadChart`: The chart data for the sprint.
    """
    sprint = sprint_service.select_sprint_by_id_db(sprint_id, user.id, session)
    return SprintReadChart.from_sprint(sprint)