from kivy.uix.popup import Popup
from modified_classes import NewFloatLayout
from kivy.properties import BooleanProperty


class MessagePopup(NewFloatLayout):
    message = None
    popup_window = None

    def __init__(self, popup_window, message=None):
        self.message = message
        self.popup_window = popup_window
        super().__init__()

def show_message_popup(message):
    popup_window = Popup(title="INFO", size_hint=(None, None), size=(400, 200))
    popup_content = MessagePopup(popup_window, message)
    popup_window.content = popup_content
    popup_window.open()


class YesNoPopup(NewFloatLayout):
    question = None
    popup_window = None
    answer = BooleanProperty(None)

    def __init__(self, popup_window, question=None):
        self.question = question
        self.popup_window = popup_window
        super().__init__()

def show_question_popup(question):
    popup_window = Popup(title="INFO", size_hint=(None, None), size=(400, 200))
    popup_content = MessagePopup(popup_window, message)
    popup_window.content = popup_content
    popup_window.open()