from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List

from therados.db.session import get_db
from therados.models.domain_models import Project, Organization
from therados.schemas.domain_schemas import ProjectRead, ProjectCreate
from therados.api.auth import get_current_user, User

router = APIRouter(prefix="/projects", tags=["Projects"])

@router.get("", response_model=List[ProjectRead])
async def list_projects(db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(Project).where(Project.archived_at == None))
    return res.scalars().all()

@router.post("", response_model=ProjectRead)
async def create_project(
    project_in: ProjectCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    project = Project(
        organization_id=project_in.organization_id,
        name=project_in.name,
        description=project_in.description,
        disease_area=project_in.disease_area,
        created_by=current_user.id
    )
    db.add(project)
    await db.commit()
    await db.refresh(project)
    return project

@router.get("/{project_id}", response_model=ProjectRead)
async def get_project(project_id: str, db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(Project).where(Project.id == project_id))
    project = res.scalar_one_or_none()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project
