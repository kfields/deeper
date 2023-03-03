import arcade

from .dimgui import Gui


class Window(arcade.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.view_stack = []

    def show_view(self, new_view):
        super().show_view(new_view)

    def push_view(self, new_view):
        #print('push_view')
        self.view_stack.append(self.current_view)
        self.show_view(new_view)

    def pop_view(self):
        #print('pop_view')
        self.show_view(self.view_stack.pop())


class GuiWindow(Window):
    def __init__(self, widgets, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.gui = Gui(self, widgets)

    def on_draw(self):
        super().on_draw()
        arcade.start_render()
        self.gui.start_render()

        self.gui.finish_render()
        arcade.finish_render()
