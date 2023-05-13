from fastapi import APIRouter, HTTPException, status, Body, Depends, Request, Path
from sqlmodel import select, update, delete

from database.connection import get_session
from models.events import Event, EventUpdate
from typing import List

event_router = APIRouter(
    tags=["Events"]
)


@event_router.get("/", response_model=List[Event], description='List all events')
async def retrieve_all_events(session=Depends(get_session)) -> List[Event]:
    statement = select(Event)
    print(statement)
    events = session.exec(statement).all()
    return events

@event_router.get("/{id}", response_model=Event, description='List event')
async def retrieve_an_event(id: int = Path(...), session=Depends(get_session)) -> Event:
    event = session.get(Event, id)
    if event:
        return event
    raise HTTPException(
          status_code=status.HTTP_404_NOT_FOUND,
          detail="Event with supplied ID does not exist"
    )

@event_router.post("/", response_model=Event, description='Create event', status_code=201)
async def create_an_event(event: Event = Body(...), session=Depends(get_session)) -> Event:
    session.add(event)
    session.commit()
    session.refresh(event)
    return event

@event_router.put("/{id}", response_model=Event, description='Update event')
async def update_an_event(id: int = Path(...), update_event: EventUpdate = Body(...),
                          session=Depends(get_session)) -> Event:
    event = session.get(Event, id)
    if event:
        event_data = update_event.dict(exclude_unset=True)
        for key, value in event_data.items():
            setattr(event, key, value)
        session.add(event)
        session.commit()
        session.refresh(event)
        return event
    raise HTTPException(
          status_code=status.HTTP_404_NOT_FOUND,
          detail="Event with supplied ID does not exist"
    )


@event_router.delete("/{id}", description='Remove event')
async def delete_an_event(id: int = Path(...), session=Depends(get_session)) -> dict:
    event = session.get(Event, id)
    if event:
        session.delete(event)
        session.commit()
        #session.refresh(event)
        return { "message": "The event is successfully deleted"}
    raise HTTPException(
          status_code=status.HTTP_404_NOT_FOUND,
          detail="Event with supplied ID does not exist"
    )