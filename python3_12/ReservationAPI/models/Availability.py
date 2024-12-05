import uuid

from datetime import datetime
from typing import Optional, TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from models.Provider import Provider


class Availability(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    provider_id: uuid.UUID = Field(foreign_key='provider.id', index=True)
    provider: Optional["Provider"] = Relationship(back_populates='available_times')
    start_time: datetime
    end_time: datetime
