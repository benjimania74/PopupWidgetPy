from pygame import Color, Surface
from Widget import *

class PanelWidget(ContainerWidget):
    def __init__(self, id: int, x: int, y: int, width: int, height: int, color: Color, parent: None | Widget, draw_surface: Surface) -> None:
        super().__init__(id, x, y, width, height, color, parent, draw_surface)

    @classmethod
    def from_dict(cls: type[T], id: int, parent: None | Widget, draw_surface: Surface, values: dict) -> T:
        get_args: list[Args_Info_Type] = [
            ("x", -1),
            ("y", -1),
            ("width", -1),
            ("height", -1),
            ("background", "#FFFFFF00", Color),
        ]
        args = cls.get_args(get_args, values)
        panelWidget = cls(id, *args, parent, draw_surface)
        panelWidget.generate_children( values.get("content", []) )
        return panelWidget