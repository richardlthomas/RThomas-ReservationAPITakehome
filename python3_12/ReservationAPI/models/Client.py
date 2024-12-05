import uuid

from sqlmodel import Field, Relationship, SQLModel

from models.Appointment import Appointment


class Client(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str = Field(index=True)
    appointments: list["Appointment"] = Relationship(back_populates='client')
