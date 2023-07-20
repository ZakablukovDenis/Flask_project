from pydantic import BaseModel


class CreateNotification(BaseModel):
    title: str
    description: str
    owner: str
