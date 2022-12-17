import imgui

from pyglet import clock
from pyglet.window import key, mouse

from .renderer import GuiRenderer
from .widget import Widget


class GuiBase(Widget):
    REVERSE_KEY_MAP = {
        key.TAB: imgui.KEY_TAB,
        key.LEFT: imgui.KEY_LEFT_ARROW,
        key.RIGHT: imgui.KEY_RIGHT_ARROW,
        key.UP: imgui.KEY_UP_ARROW,
        key.DOWN: imgui.KEY_DOWN_ARROW,
        key.PAGEUP: imgui.KEY_PAGE_UP,
        key.PAGEDOWN: imgui.KEY_PAGE_DOWN,
        key.HOME: imgui.KEY_HOME,
        key.END: imgui.KEY_END,
        key.DELETE: imgui.KEY_DELETE,
        key.SPACE: imgui.KEY_SPACE,
        key.BACKSPACE: imgui.KEY_BACKSPACE,
        key.RETURN: imgui.KEY_ENTER,
        key.ESCAPE: imgui.KEY_ESCAPE,
        key.A: imgui.KEY_A,
        key.C: imgui.KEY_C,
        key.V: imgui.KEY_V,
        key.X: imgui.KEY_X,
        key.Y: imgui.KEY_Y,
        key.Z: imgui.KEY_Z,
    }

    def _map_keys(self):
        key_map = self.io.key_map

        # note: we cannot use default mechanism of mapping keys
        #       because pyglet uses weird key translation scheme
        for value in self.REVERSE_KEY_MAP.values():
            key_map[value] = value

    def _on_mods_change(self, mods):
        self.io.key_ctrl = mods & key.MOD_CTRL
        self.io.key_super = mods & key.MOD_COMMAND
        self.io.key_alt = mods & key.MOD_ALT
        self.io.key_shift = mods & key.MOD_SHIFT

    def on_key_press(self, key_pressed, mods):
        if key_pressed in self.REVERSE_KEY_MAP:
            self.io.keys_down[self.REVERSE_KEY_MAP[key_pressed]] = True
        self._on_mods_change(mods)

    def on_key_release(self, key_released, mods):
        if key_released in self.REVERSE_KEY_MAP:
            self.io.keys_down[self.REVERSE_KEY_MAP[key_released]] = False
        self._on_mods_change(mods)

    def on_text(self, text):
        io = imgui.get_io()

        for char in text:
            io.add_input_character(ord(char))

    def on_mouse_motion(self, x, y, dx, dy):
        self.io.mouse_pos = x, self.io.display_size.y - y
        if self.io.want_capture_mouse:
            return True

    def on_mouse_drag(self, x, y, dx, dy, button, modifiers):
        self.io.mouse_pos = x, self.io.display_size.y - y

        if button == mouse.LEFT:
            self.io.mouse_down[0] = 1

        if button == mouse.RIGHT:
            self.io.mouse_down[1] = 1

        if button == mouse.MIDDLE:
            self.io.mouse_down[2] = 1

    def on_mouse_press(self, x, y, button, modifiers):
        self.io.mouse_pos = x, self.io.display_size.y - y

        if button == mouse.LEFT:
            self.io.mouse_down[0] = 1

        if button == mouse.RIGHT:
            self.io.mouse_down[1] = 1

        if button == mouse.MIDDLE:
            self.io.mouse_down[2] = 1

    def on_mouse_release(self, x, y, button, modifiers):
        self.io.mouse_pos = x, self.io.display_size.y - y

        code = 0; delay = .2
        if button == mouse.LEFT:
            delay = 0
        elif button == mouse.RIGHT:
            code = 1
        elif button == mouse.MIDDLE:
            code = 2
        # Need a slight delay for touch events
        def set_mouse(delta_time):
            self.io.mouse_down[code] = 0
        clock.schedule_once(set_mouse, delay)

    def on_mouse_scroll(self, x, y, mods, scroll):
        self.io.mouse_wheel = scroll

    def on_resize(self, width, height):
        self.io.display_size = width, height


class Gui(GuiBase):
    def __init__(self, window, children=[], auto_enable=True):
        self.window = window
        super().__init__(children)
        # Must create or set the context before instantiating the renderer
        imgui.create_context()
        self.io = imgui.get_io()

        self.renderer = GuiRenderer(window)

        if auto_enable:
            self.enable()
        else:
            window.push_handlers(self.on_resize)

    def enable(self):
        self.window.push_handlers(self)

    def disable(self):
        self.window.remove_handlers(self)

    def add_child(self, child):
        super().add_child(child)
        child.create(self)

    def load_font(self, font_path):
        io = imgui.get_io()
        new_font = io.fonts.add_font_from_file_ttf(str(font_path), 20)
        self.renderer.refresh_font_texture()

    def start_render(self):
        imgui.new_frame()

    def finish_render(self):
        self.draw()
        imgui.end_frame()
        imgui.render()
        self.renderer.render(imgui.get_draw_data())
