from pydantic import BaseModel


class PreferenceCategoryCreate(BaseModel):
    name: str
    description: str


class PreferenceCategory(PreferenceCategoryCreate):
    id: int
    is_active: bool
