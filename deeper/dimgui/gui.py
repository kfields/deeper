import imgui

from pyglet import clock
from pyglet import event
from pyglet.window import key, mouse

from .renderer import GuiRenderer
from .widget import Widget
from .board import Clipboard, Dropboard

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

        if self.io.want_capture_keyboard:
            return event.EVENT_HANDLED

    def on_key_release(self, key_released, mods):
        if key_released in self.REVERSE_KEY_MAP:
            self.io.keys_down[self.REVERSE_KEY_MAP[key_released]] = False
        self._on_mods_change(mods)

        if self.io.want_capture_keyboard:
            return event.EVENT_HANDLED

    def on_text(self, text):
        io = imgui.get_io()

        for char in text:
            io.add_input_character(ord(char))

        if self.io.want_text_input:
        #if self.io.want_text_input or self.io.want_capture_keyboard:
            return event.EVENT_HANDLED

    def on_mouse_motion(self, x, y, dx, dy):
        self.io.mouse_pos = x, self.io.display_size.y - y
        if self.io.want_capture_mouse:
            return event.EVENT_HANDLED

    def on_mouse_drag(self, x, y, dx, dy, button, modifiers):
        self.io.mouse_pos = x, self.io.display_size.y - y

        if button == mouse.LEFT:
            self.io.mouse_down[0] = 1

        if button == mouse.RIGHT:
            self.io.mouse_down[1] = 1

        if button == mouse.MIDDLE:
            self.io.mouse_down[2] = 1

        if self.io.want_capture_mouse:
            return event.EVENT_HANDLED

    def on_mouse_press(self, x, y, button, modifiers):
        self.io.mouse_pos = x, self.io.display_size.y - y

        if button == mouse.LEFT:
            self.io.mouse_down[0] = 1

        if button == mouse.RIGHT:
            self.io.mouse_down[1] = 1

        if button == mouse.MIDDLE:
            self.io.mouse_down[2] = 1

        if self.io.want_capture_mouse:
            return event.EVENT_HANDLED

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

        if self.io.want_capture_mouse:
            return event.EVENT_HANDLED

    def on_mouse_scroll(self, x, y, mods, scroll):
        self.io.mouse_wheel = scroll
        if self.io.want_capture_mouse:
            return event.EVENT_HANDLED

    def on_resize(self, width, height):
        self.io.display_size = width, height

    #Helpers
    def is_key_down(self, key):
        return self.io.keys_down[key]

class Gui(GuiBase):
    context = None
    renderer = None
    def __init__(self, window, children=[], auto_enable=True):
        self.window = window
        super().__init__(children)
        self.default_font = None
        self.clipboard = Clipboard()
        self.dropboard = Dropboard()
        # Must create or set the context before instantiating the renderer
        # Note: Definitely need to share the renderer to use gui per view.
        # Since the renderer is tied to the context we need to share that also.
        if not self.context:
            #print("create_context")
            imgui.create_context()
            Gui.context = imgui.get_current_context()

        self.io = imgui.get_io()
        self._map_keys()

        if not self.renderer:
            Gui.renderer = GuiRenderer(window)

        if auto_enable:
            self.enable()
        else:
            window.push_handlers(self.on_resize)

    #def __del__(self):
    #    imgui.destroy_context(self.context)

    def enable(self):
        #imgui.set_current_context(self.context)
        self.window.push_handlers(self)

    def disable(self):
        self.window.remove_handlers(self)

    def show(self):
        #imgui.set_current_context(self.context)
        pass

    def hide(self):
        pass

    def add_child(self, child):
        super().add_child(child)
        child.create(self)
        return child

    def load_font(self, font_path, font_pixel_size):
        io = imgui.get_io()
        font = io.fonts.add_font_from_file_ttf(str(font_path), font_pixel_size)
        self.renderer.refresh_font_texture()
        return font

    def start_render(self):
        #imgui.set_current_context(self.context)
        imgui.new_frame()
        if self.default_font:
            imgui.push_font(self.default_font)

    def finish_render(self):
        #imgui.set_current_context(self.context)
        self.draw()
        if self.default_font:
            imgui.pop_font()
        imgui.end_frame()
        imgui.render()
        self.renderer.render(imgui.get_draw_data())

class ViewGui(Gui):
    def __init__(self, view, children=[], auto_enable=True):
        self.view = view
        super().__init__(view.window, children, auto_enable)
