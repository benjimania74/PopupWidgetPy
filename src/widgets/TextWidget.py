from pygame import Color, Surface, font
from Widget import *
from Event import *

from typing import Any

class TextWidget(Widget):
    text: str
    text_color: Color
    font_file: str|None
    font_size: int

    def __init__(self, id: int, x: int, y: int, width: int, height: int, text: str, background_color: Color, text_color: Color, font_file: str|None, font_size: int, parent: Widget, draw_surface: Surface) -> None:
        super().__init__(id, x, y, width, height, background_color, parent, draw_surface)
        self.text = text
        self.text_color = text_color
        self.font_file = font_file
        self.font_size = font_size
    
    def show(self) -> None:
        self.widget_surface.fill(self.background_color)
        text_font: font.Font = font.Font(self.font_file, self.font_size)
        text_surface: Surface = text_font.render(self.text, False, self.text_color)
        self.widget_surface.blit(
            text_surface,
            (
                self.widget_surface.get_width() // 2 - text_surface.get_width() // 2,
                self.widget_surface.get_height() // 2 - text_surface.get_height() // 2
            )
        )
        self.draw_surface.blit(
            self.widget_surface,
            (self.x, self.y)
        )

    @classmethod
    def from_dict(cls: type[T], id: int, parent: None | Widget, draw_surface: Surface, values: dict) -> T:
        get_list: list[tuple] = [
            ("x", -1),
            ("y",-1),
            ("width", -1),
            ("height", -1),
            ("text", ""),
            ("background", "#00000000", Color),
            ("color", "#000000", Color),
            ("font_name", None),
            ("font_size", 32),
        ]

        args: list[Any] = cls.get_args(get_list, values)
        return cls(id, *args, parent, draw_surface)

    def on_init(self, info: Event):
        print(info.get_type(), "-", info.get_info())