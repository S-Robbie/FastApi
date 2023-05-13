from fastapi import APIRouter, HTTPException, status, Body
from models.users import User, UserSignIn
from models.events import Event
from typing import List

event_router = APIRouter(
    tags=["Events"]
)

events = []

@event_router.get("/", response_model=List[Event], description='List all events')
async def retrieve_all_events() -> List[Event]:
    return events

@event_router.get("/{id}", response_model=Event, description='List event')
async def retrieve_an_event(id: int) -> Event:
    for event in events:
        if id == event.id:
            return event
    raise HTTPException(
          status_code=status.HTTP_404_NOT_FOUND,
          detail="Event with supplied ID does not exist"
    )

@event_router.post("/", response_model=Event, description='Create event', status_code=201)
async def create_an_event(event: Event = Body(...)) -> Event:
    event.id = len(events) + 1
    events.append(event)
    return event

@event_router.put("/{id}", response_model=Event, description='Update event')
async def update_an_event(id: int, event: Event = Body(...)) -> Event:
    for idx, eve in enumerate(events):
        if id == eve.id:
            event.id = id
            events[idx] = event
            return event
    raise HTTPException(
          status_code=status.HTTP_404_NOT_FOUND,
          detail="Event with supplied ID does not exist"
    )

@event_router.delete("/",  description='Remove all events')
async def delete_all_events() -> dict:
    events.clear()
    return {"message": "All events removed successfully" }

@event_router.delete("/{id}", description='Remove event')
async def delete_an_event(id: int) -> dict:
    for event in events:
        if id == event.id:
            events.remove(event)
            return {
                "message": "Event deleted successfully"
            }
    raise HTTPException(
          status_code=status.HTTP_404_NOT_FOUND,
          detail="Event with supplied ID does not exist"
    )