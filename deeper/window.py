import arcade


class Window(arcade.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def show_view(self, new_view):
        super().show_view(new_view)
