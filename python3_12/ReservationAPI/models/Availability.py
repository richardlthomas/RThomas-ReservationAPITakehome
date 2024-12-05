import uuid

from datetime import datetime

from sqlmodel import Field, Relationship, SQLModel

from models.Provider import Provider


class Availability(SQLModel):
    provider_id: uuid.UUID = Field(foreign_key='provider.id', index=True)
    provider: Provider = Relationship(back_populates='availabile_times')
    start_time: datetime
    end_time: datetime
