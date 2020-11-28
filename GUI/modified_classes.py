from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.properties import ListProperty

from kivy.factory import Factory
from kivy.lang import Builder



Builder.load_string("""
<NewGridLayout>:
    back_color: 1,1,1,1
    canvas.before:
        Color:
            rgba: self.back_color
        Rectangle:
            pos: self.pos
            size: self.size
""")

class NewGridLayout(GridLayout):
    back_color = ListProperty([1,1,1,1])

Factory.register('modified_classes', module='NewGridLayout')



Builder.load_string("""
<NewBoxLayout>:
    back_color: 1,1,1,1
    canvas.before:
        Color:
            rgba: self.back_color
        Rectangle:
            pos: self.pos
            size: self.size
""")

class NewBoxLayout(BoxLayout):
    back_color = ListProperty([1,1,1,1])

Factory.register('modified_classes', module='NewBoxLayout')




Builder.load_string("""
<NewFloatLayout>:
    back_color: 1,1,1,1
    canvas.before:
        Color:
            rgba: self.back_color
        Rectangle:
            pos: self.pos
            size: self.size
""")

class NewFloatLayout(FloatLayout):
    back_color = ListProperty([1,1,1,1])

Factory.register('modified_classes', module='NewFloatLayout')


class DataButton(Button):

    def __init__(self, data, **kwargs):
        super(DataButton, self).__init__(**kwargs)
        self.data = data