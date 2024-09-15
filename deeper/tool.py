import time

from crunge.engine.view import View
from crunge.engine.dispatcher import Dispatcher

class Tool(Dispatcher):
    def __init__(self, view: View, title='') -> None:
        self.view = view
        self.gui = view.gui
        self.window = view.window
        self.title = title
        self._click_time = time.time()
        self._click_count = 0

    def enable(self):
        #self.window.push_handlers(self)
        pass

    def disable(self):
        #self.window.remove_handlers(self)
        pass

    def on_mouse_motion(self, x: int, y: int, dx: int, dy: int):
        pass

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        t = time.time()
        if t - self._click_time < 0.25:
            self._click_count += 1
        else:
            self._click_count = 1
        #print(self._click_count)
        self._click_time = time.time()
