from pygame import Color, Surface
from Widget import *
from Event import *

class TextWidget(Widget):
    text: str
    font_file: str|None
    font_size: int

    def __init__(self, id: int, x: int, y: int, width: int, height: int, text: str, background_color: Color, text_color: Color, font_file: str|None, font_size: int, parent: None | Widget, draw_surface: Surface) -> None:
        super().__init__(id, x, y, width, height, background_color, parent, draw_surface)
        self.text = text
        self.text_color = text_color
        self.font_file = font_file
        self.font_size = font_size
    
    @classmethod
    def from_dict(cls: type[T], id: int, parent: None | Widget, draw_surface: Surface, values: EventInfo) -> T:
        return cls(id, -1,-1,50,50,"test",Color(0,255,0),Color(0,0,0), None, 32, parent, draw_surface)

    def on_init(self, info: Event):
        print(info.get_type(), "-", info.get_info())