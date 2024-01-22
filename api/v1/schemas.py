from pydantic import BaseModel, UUID4


class MenuDTO(BaseModel):
    id: UUID4
    title: str
    description: str

