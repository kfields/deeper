import arcade

from .dimgui import Gui

class ArcadeContextState:
    def __init__(self, ctx: arcade.ArcadeContext) -> None:
        self.viewport = ctx.viewport
        self.projection_2d_matrix =  ctx.projection_2d_matrix
        self.view_matrix_2d = ctx.view_matrix_2d

    def restore(self, ctx: arcade.ArcadeContext) -> None:
        ctx.viewport = self.viewport
        ctx.projection_2d_matrix = self.projection_2d_matrix
        if self.view_matrix_2d:
            ctx.view_matrix_2d = self.view_matrix_2d

class Window(arcade.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.view_stack = []
        self.ctx_state_stack = []

    def push_ctx_state(self):
        self.ctx_state_stack.append(ArcadeContextState(self.ctx))

    def pop_ctx_state(self):
        state = self.ctx_state_stack.pop()
        state.restore(self.ctx)

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
