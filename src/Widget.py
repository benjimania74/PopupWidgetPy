from __future__ import annotations
from typing import TypeVar, Type
T = TypeVar("T", bound="Widget")

from pygame import Surface, Color, SRCALPHA

from Event import Event,EventType

class Widget:
    id: int
    x: int
    y: int
    width: int
    height: int
    color: Color

    parent: None|Widget

    draw_surface: Surface

    childs: dict[int,Widget] = {}

    def __init__(self, id:int, x:int, y:int, width:int, height:int, color: Color, parent:None|Widget, draw_surface: Surface) -> None:
        self.id = id
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.parent = parent
        self.draw_surface = draw_surface

        for event_type in EventType:
            if event_type.value == None: continue
            method_name: str = "on_" + str(event_type.value)
            if hasattr(self, method_name): continue                               # if a method (or an attribute) already exists with the same name
            def on_event(self: Widget, event: Event):                             # default event method
                return True
            self.__setattr__(method_name, on_event)                               # add the method to the object
        self.on_event( Event( EventType.INIT_EVENT, {"id": id}) )                 # on init event call

    def append_child(self, widget: Widget) -> None:
        """Add a child to this widget"""
        self.childs[widget.id] = widget
    
    def remove_child(self, widget_id: int) -> None:
        """Remove a child from this widget"""
        self.childs.pop(widget_id)

    def show(self) -> None:
        """Show to the draw surface the widget"""
        to_draw: Surface = Surface( (0,0), SRCALPHA )
        to_draw.fill(self.color)
        self.draw_surface.blit(to_draw, (self.x,self.y))

    @classmethod
    def from_dict(cls: Type[T], id:int, parent:None|Widget, draw_surface:Surface, values:dict) -> T:
        """Generate a Widget from a JSON data (as dict)"""
        x:int = values.get("x", 0) + parent.x if parent != None else 0
        y:int = values.get("y", 0) + parent.y if parent != None else 0
        width:int = values.get("width", 0)
        height:int = values.get("height", 0)
        color:Color = Color(values.get("background", "#FFFFFF00"))
        return cls(id,x,y,width,height,color,parent,draw_surface)

    def on_event(self, event:Event) -> None:
        """Trigger an event"""
        if event.get_type() == None: return
        event_method_name = "on_" + str(event.get_type().value)
        event_method = self.__getattribute__(event_method_name)                    # always exists (generate at the init) -> dev is supposed to do his job well so this method is always right writted
        if not event_method(event) and self.parent != None:                        # propagate if "asked" and possible
            self.parent.on_event(event)
