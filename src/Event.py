from enum import Enum
from typing import Union, Sequence

valueType = Union[int,float,str]
dataType = Union[valueType, dict[str,valueType], Sequence[valueType]]

EventInfo = dict[str,dataType]

class EventType(Enum):
    NONE = None
    INIT_EVENT = "init"
    HOVER_EVENT = "hover"
    CLICK_EVENT = "click"

class Event:
    event_type: EventType
    event_info: EventInfo

    def __init__(self, event_type: EventType = EventType.NONE, event_info: EventInfo = {}) -> None:
        self.event_type = event_type
        self.event_info = event_info
    
    def get_type(self) -> EventType:
        return self.event_type
    def get_info(self) -> EventInfo:
        return self.event_info