import arcade


class Window(arcade.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.view_stack = []

    def show_view(self, new_view):
        super().show_view(new_view)

    def push_view(self, new_view):
        print('push_view')
        self.view_stack.append(self.current_view)
        self.show_view(new_view)

    def pop_view(self):
        print('pop_view')
        self.show_view(self.view_stack.pop())
