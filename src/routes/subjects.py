from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from database import get_session
from src.schemas.subject import SubjectCreate, SubjectUpdate, SubjectRead
from src.services.subject_service import SubjectService
from src.dependencies.auth import get_current_user
from src.Models.user import User

router = APIRouter(prefix="/subjects", tags=["Subjects"])

@router.post("/", response_model=SubjectRead, status_code=status.HTTP_201_CREATED)
def create_subject(
    subject_create: SubjectCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    return SubjectService.create_subject(session, subject_create, current_user.id)

@router.get("/", response_model=list[SubjectRead])
def list_subjects(
    skip: int = 0,
    limit: int = 100,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    return SubjectService.get_subjects(session, skip, limit)

@router.get("/my", response_model=list[SubjectRead])
def my_subjects(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    return SubjectService.get_subjects_by_owner(session, current_user.id)

@router.get("/{subject_id}", response_model=SubjectRead)
def get_subject(
    subject_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    subject = SubjectService.get_subject(session, subject_id)
    if not subject:
        raise HTTPException(status_code=404, detail="Subject not found")
    return subject

@router.put("/{subject_id}", response_model=SubjectRead)
def update_subject(
    subject_id: int,
    subject_update: SubjectUpdate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    subject = SubjectService.get_subject(session, subject_id)
    if not subject:
        raise HTTPException(status_code=404, detail="Subject not found")
    if subject.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this subject")
    return SubjectService.update_subject(session, subject, subject_update)

@router.delete("/{subject_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_subject(
    subject_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    subject = SubjectService.get_subject(session, subject_id)
    if not subject:
        raise HTTPException(status_code=404, detail="Subject not found")
    if subject.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this subject")
    SubjectService.delete_subject(session, subject_id)
    return None