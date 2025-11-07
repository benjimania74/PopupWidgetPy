from pygame import Color, Surface
from Widget import *

class PanelWidget(ContainerWidget):
    def __init__(self, id: int, x: int, y: int, width: int, height: int, color: Color, parent: None | Widget, draw_surface: Surface) -> None:
        super().__init__(id, x, y, width, height, color, parent, draw_surface)

    @classmethod
    def from_dict(cls: type[T], id: int, parent: None | Widget, draw_surface: Surface, values: dict) -> T:
        x:int = values.get("x", -1)
        y:int = values.get("y", -1)
        width:int = values.get("width",0)
        height:int = values.get("height",0)
        color: Color = Color( values.get("background", "#FFFFFF00") )
        panelWidget = cls(id, x, y, width, height, color, parent, draw_surface)
        cls.generate_children( panelWidget, values.get("content", []) )
        return panelWidget