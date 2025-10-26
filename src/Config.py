from sys import path
import json

from Widget import Widget

NAME: str = "PopupWidgetPy"

class Config:
    width:int
    height:int
    x:int
    y:int
    start_panel:str

    panels: list[Widget] = []

    def __init__(self, screen_size: tuple[int,int]) -> None:
        CONFIG_NAME = path[0] + "/../config.json"
        try:
            config_file = open(CONFIG_NAME, "r")
            config = json.loads(config_file.read())

            def get_int(att:str) -> int:
                return config.get(att,0)

            self.width = get_int("width")
            self.height = get_int("height")
            self.x = get_int("x")
            self.y = get_int("y")

            self.start_panel = config.get("start_panel", "")
        except:
            raise Exception("Config file not found or misdefined")