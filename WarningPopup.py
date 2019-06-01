from kivy.uix.popup import Popup
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.uix.label import Label


class WarningPopup(Popup):
    def __init__(self, text, **kwargs):
        super(WarningPopup, self).__init__(**kwargs)
        self.content = Label(text=text)
        self.size_hint = (0.3, 0.2)

        self.open()
        Clock.schedule_once(self.fade, 2)

    def fade(self, duration):
        anim = Animation(background_color=[1, 1, 1, 0], duration=duration // 1.2)
        anim.on_complete(self.dismiss)
        anim.start(self)
        del self
