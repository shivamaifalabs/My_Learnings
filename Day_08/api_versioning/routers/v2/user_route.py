from fastapi import APIRouter

router = APIRouter(prefix="/v2/users", tags=["Users : v2"])

@router.get("/")
def get_users_v2():
    return {
        "total": 2,
        "users": [
            {"id": 1, "name": "Shivam", "status": "active"},
            {"id": 2, "name": "Virat", "status": "inactive"},
        ]
    }
