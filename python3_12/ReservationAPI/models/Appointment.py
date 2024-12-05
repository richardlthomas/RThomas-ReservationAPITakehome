import uuid

from datetime import datetime, UTC
from typing import Optional, TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from models.Client import Client
    from models.Provider import Provider


class Appointment(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    client_id: uuid.UUID = Field(foreign_key='client.id', index=True)
    client: Optional["Client"] = Relationship(back_populates='appointments')
    provider_id: uuid.UUID = Field(foreign_key='provider.id', index=True)
    provider: Optional["Provider"] = Relationship(back_populates='appointments')
    appointment_time: datetime = Field(index=True)
    is_confirmed: bool = Field(default=False)
    created_on: datetime = Field(default=datetime.now(UTC))
