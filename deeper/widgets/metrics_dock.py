from loguru import logger

from crunge import imgui

from crunge.engine.imgui.widget import Dock


class MetricsDock(Dock):
    def __init__(self, on_close: callable = None):
        super().__init__("Metrics", on_close=on_close, native=True)

    def _begin(self):
        opened = imgui.show_metrics_window(self.closable)[0]
        # logger.debug(f"MetricsDock opened: {opened}")
        if not opened:
            self.on_close()
