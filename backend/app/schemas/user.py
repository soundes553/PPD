from pydantic import BaseModel

class UserBase(BaseModel):
    age: int
    country: str
    delivery_type: str
    education_level: str
    income_level: str
    partner_support_level: int
    family_support_level: int
    total_support_score: int
    recent_birth: bool


class UserCreate(UserBase):
    pass


class UserResponse(UserBase):
    user_id: int

    class Config:
        orm_mode = True
