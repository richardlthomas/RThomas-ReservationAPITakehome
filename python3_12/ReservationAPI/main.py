import os
import uuid

import uvicorn

from datetime import datetime, timedelta
from typing import Annotated, Sequence
from uuid import UUID

from models.Appointment import Appointment
from models.Availability import Availability
from models.Client import Client
from models.Provider import Provider

from dotenv import load_dotenv
from fastapi import Body, Depends, FastAPI, HTTPException
from sqlmodel import create_engine, select, Session, SQLModel

load_dotenv()

DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_USERNAME = os.getenv('DB_USERNAME')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME')

db_uri = f'postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?sslmode=require'
connect_args = {}
engine = create_engine(db_uri, connect_args=connect_args)

APPOINTMENT_LENGTH = int(os.getenv('APPOINTMENT_LENGTH_IN_MINUTES'))


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]

app = FastAPI()


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.get("/")
async def home():
    return {'msg': 'Thank you for using the Henry Meds Reservation System!'}


@app.get('/providers/')
async def get_providers(
        session: SessionDep
) -> Sequence[Provider]:
    providers = session.exec(select(Provider)).all()
    return providers


@app.post('/providers/')
async def add_provider(provider: Provider, session: SessionDep) -> Provider:
    db_provider = Provider.model_validate(provider)
    session.add(db_provider)
    session.commit()
    session.refresh(db_provider)
    return db_provider


@app.get('/providers/{provider_id}/')
async def get_provider(provider_id: uuid.UUID, session: SessionDep) -> Provider:
    provider = session.get(Provider, provider_id)
    if not provider:
        raise HTTPException(status_code=404, detail='Provider not found')
    return provider


@app.get('/providers/{provider_id}/availability/')
async def get_provider_availability(provider_id: uuid.UUID, session: SessionDep) -> list[datetime]:
    provider_availability = session.exec(select(Availability).where(Availability.provider_id == provider_id)).all()
    available_appointments = []
    for available_window in provider_availability:
        start = available_window.start_time
        end = available_window.end_time
        delta = timedelta(minutes=APPOINTMENT_LENGTH)
        current = start
        while current < end:
            available_appointments.append(current)
            current += delta
    return available_appointments


@app.post('/providers/{provider_id}/availability/')
async def add_provider_availability(
        provider_id: uuid.UUID,
        available_from: Annotated[datetime, Body()],
        available_to: Annotated[datetime, Body()],
        session: SessionDep) -> Sequence[Availability]:
    provider = await get_provider(provider_id, session)
    availability = Availability(
        provider_id=provider_id,
        provider=provider,
        start_time=available_from,
        end_time=available_to
    )
    db_availability = Availability.model_validate(availability)
    session.add(db_availability)
    session.commit()
    session.refresh(db_availability)
    current_availability = await get_provider_availability(provider_id, session)
    return current_availability


@app.get('/clients/')
async def get_clients(
        session: SessionDep
) -> Sequence[Client]:
    clients = session.exec(select(Client)).all()
    return clients


@app.post('/clients/')
async def add_client(client: Client, session: SessionDep) -> Client:
    db_client = Client.model_validate(client)
    session.add(db_client)
    session.commit()
    session.refresh(db_client)
    return db_client


@app.get('/clients/{client_id}')
async def get_client(client_id: uuid.UUID, session: SessionDep) -> Client:
    client = session.get(Client, client_id)
    if not client:
        raise HTTPException(status_code=404, detail='Client not found')
    return client


@app.post('/appointments/reserve')
async def reserve_appointment(
        client_id: Annotated[UUID, Body()],
        provider_id: Annotated[UUID, Body()],
        appointment_time: Annotated[datetime, Body()],
        session: SessionDep) -> Appointment:
    time = appointment_time
    client = await get_client(client_id, session)
    provider = await get_provider(provider_id, session)
    available_appointments = await get_provider_availability(provider_id, session)
    appointment = Appointment(client=client,
                              client_id=client_id,
                              provider=provider,
                              provider_id=provider_id,
                              appointment_time=appointment_time)
    db_appointment = Appointment.model_validate(appointment)
    if time not in available_appointments:
        raise HTTPException(status_code=400, detail='Time requested is not available, please see provider availability')
    else:
        session.add(db_appointment)
        session.commit()
        session.refresh(db_appointment)
        return db_appointment


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
