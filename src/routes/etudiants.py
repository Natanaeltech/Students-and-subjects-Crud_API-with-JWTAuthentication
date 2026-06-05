from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from database import get_session
from src.schemas.etudiant import EtudiantCreate, EtudiantUpdate, EtudiantRead
from src.services.etudiant_service import EtudiantService
from src.dependencies.auth import get_current_user
from src.Models.user import User

router = APIRouter(prefix="/etudiants", tags=["Etudiants"])

@router.post("/", response_model=EtudiantRead, status_code=status.HTTP_201_CREATED)
def create_etudiant(
    etudiant_create: EtudiantCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    return EtudiantService.create_etudiant(session, etudiant_create, current_user.id)

@router.get("/", response_model=list[EtudiantRead])
def list_etudiants(
    skip: int = 0,
    limit: int = 100,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    return EtudiantService.get_etudiants(session, skip, limit)

@router.get("/my", response_model=list[EtudiantRead])
def my_etudiants(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    return EtudiantService.get_etudiants_by_owner(session, current_user.id)

@router.get("/{etudiant_id}", response_model=EtudiantRead)
def get_etudiant(
    etudiant_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    etudiant = EtudiantService.get_etudiant(session, etudiant_id)
    if not etudiant:
        raise HTTPException(status_code=404, detail="Etudiant not found")
    return etudiant

@router.put("/{etudiant_id}", response_model=EtudiantRead)
def update_etudiant(
    etudiant_id: int,
    etudiant_update: EtudiantUpdate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    etudiant = EtudiantService.get_etudiant(session, etudiant_id)
    if not etudiant:
        raise HTTPException(status_code=404, detail="Etudiant not found")
    if etudiant.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this etudiant")
    return EtudiantService.update_etudiant(session, etudiant, etudiant_update)

@router.delete("/{etudiant_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_etudiant(
    etudiant_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    etudiant = EtudiantService.get_etudiant(session, etudiant_id)
    if not etudiant:
        raise HTTPException(status_code=404, detail="Etudiant not found")
    if etudiant.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this etudiant")
    EtudiantService.delete_etudiant(session, etudiant_id)
    return None