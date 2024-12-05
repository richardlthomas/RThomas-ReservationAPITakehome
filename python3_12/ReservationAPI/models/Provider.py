import uuid

from typing import List, TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from models.Appointment import Appointment
    from models.Availability import Availability


class Provider(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str = Field(index=True)
    appointments: List["Appointment"] = Relationship(back_populates='provider')
    available_times: List["Availability"] = Relationship(back_populates='provider')
