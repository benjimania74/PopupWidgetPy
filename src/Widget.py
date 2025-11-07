from __future__ import annotations
from typing import TypeVar, Type, final
from abc import ABC, abstractmethod
from importlib import import_module

from pygame import Surface, Color, SRCALPHA

from Event import Event,EventType

T = TypeVar("T", bound="Widget")

class Widget(ABC):
    id: int
    x: int
    y: int
    width: int
    height: int
    color: Color

    parent: None|Widget

    draw_surface: Surface

    widget_surface: Surface

    def __init__(self, id:int, x:int, y:int, width:int, height:int, color: Color, parent:None|Widget, draw_surface: Surface) -> None:
        self.id = id
        self.x = x if x != -1 else draw_surface.get_width() // 2 - width // 2     # if x = -1 -> auto center horizontaly
        self.y = y if y != -1 else draw_surface.get_height() // 2 - height // 2   # if y = -1 -> auto center verticaly
        self.width = width
        self.height = height
        self.color = color
        self.parent = parent
        self.draw_surface = draw_surface
        self.widget_surface = Surface( (width, height), SRCALPHA )

        for event_type in EventType:
            if event_type.value == None: continue
            method_name: str = "on_" + str(event_type.value)
            if hasattr(self, method_name): continue                               # if a method (or an attribute) already exists with the same name
            def on_event(event: Event):                                           # default event method
                return True
            self.__setattr__(method_name, on_event)                               # add the method to the object
        self.on_event( Event( EventType.INIT_EVENT, {"id": id}) )                 # on init event call

    def show(self) -> None:
        """Show to the draw surface the widget"""
        self.widget_surface.fill(self.color)
        self.draw_surface.blit(self.widget_surface, (self.x,self.y))

    @classmethod
    @abstractmethod
    def from_dict(cls: Type[T], id:int, parent:None|Widget, draw_surface:Surface, values:dict) -> T:
        """Generate a Widget from a JSON data (as dict)"""
        pass

    def on_event(self, event:Event) -> None:
        """Trigger an event"""
        if event.get_type() == None: return
        event_method_name = "on_" + str(event.get_type().value)
        event_method = self.__getattribute__(event_method_name)                    # always exists (generate at the init) -> dev is supposed to do his job well so this method is always right writted
        if not event_method(event) and self.parent != None:                        # propagate if "asked" and possible
            self.parent.on_event(event)

class ContainerWidget(Widget):
    content: list[Widget]
    children: dict[int, Widget]

    def __init__(self, id: int, x: int, y: int, width: int, height: int, color: Color, parent: None | Widget, draw_surface: Surface) -> None:
        super().__init__(id, x, y, width, height, color, parent, draw_surface)
        self.content = []
        self.children = {}
    
    @classmethod
    @final
    def generate_children(cls, container: ContainerWidget, children_data: list[dict]):
        """Generate the list of children of the Widget"""
        children: list[Widget] = []
        child_number: int = 1
        for child_data in children_data:
            class_type = child_data["type"]
            try:
                child_module = import_module("widgets." + class_type, "src")        # Import the module where the Widget is supposed to be
                child_class = getattr(child_module, class_type)                     # Get the class of the Widget
                if child_class == None: continue                                    # If the class does not exists then it cannot be a Widget
                child = child_class.from_dict(                                      # Generate the child widget
                    container.id * 100 + child_number,
                    container,
                    container.widget_surface,
                    child_data
                )
                children.append(child)
                child_number += 1
            except:
                pass
        container.append_child(*children)

    def append_child(self, *widgets: Widget) -> None:
        """Add a child to this widget"""
        for widget in widgets:
            self.children[widget.id] = widget
    
    def remove_child(self, widget_id: int) -> None:
        """Remove a child from this widget"""
        self.children.pop(widget_id)
    
    def show(self) -> None:
        super().show()
        for child in self.children.values():
            child.show()