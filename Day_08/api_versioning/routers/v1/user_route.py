from fastapi import APIRouter

router = APIRouter(prefix="/v1/users", tags=["Users : v1"])

@router.get("/")
def get_users_v1():
    return [
        {"id": 1, "name": "Shivam"},
        {"id": 2, "name": "Virat"}
    ]
