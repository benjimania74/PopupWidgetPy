import json

from pygame import Surface
from widgets.PanelWidget import PanelWidget

NAME: str = "PopupWidgetPy"

class Config:
    width:int
    height:int
    x:int
    y:int
    start_panel:str

    panels: dict[str, PanelWidget] = {}

    panels_config: dict = {}

    def __init__(self, config_path:str, screen_size:tuple[int,int]) -> None:
        try:
            config_file = open(config_path, "r")
            config = json.loads(config_file.read())

            def get_int(att:str) -> int:
                return config.get(att,0)

            self.width = get_int("width")
            self.height = get_int("height")
            self.x = get_int("x")
            self.y = get_int("y")

            self.start_panel = config.get("start_panel", "")

            self.panels_config = config.get("panels", {})
        except:
            raise Exception("Config file not found or misdefined")
    
    def load_panels(self, default_surface:Surface) -> None:
        """Load panels from the config"""
        id:int = 0
        for panel_config in self.panels_config.items():
            self.panels[panel_config[0]] = PanelWidget.from_dict(id, None, default_surface, panel_config[1])
            id += 1