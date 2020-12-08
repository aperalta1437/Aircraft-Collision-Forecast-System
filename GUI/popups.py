from kivy.app import App
from kivy.uix.popup import Popup
from GUI.modified_classes import NewFloatLayout
from kivy.properties import BooleanProperty
from kivy.uix.modalview import ModalView
from kivy.properties import ObjectProperty


class MessagePopup(NewFloatLayout):
    # message = None
    # popup_window = None
    btn_close_message_popup = ObjectProperty(None)
    lbl_message_popup = ObjectProperty(None)
    def __init__(self, popup_window, message=None):
        self.message = message
        self.popup_window = popup_window
        super().__init__()


def show_message_popup(message, width_hint=0.33, height_hint=0.33):
    popup_window = Popup(title="INFO", size_hint=(width_hint, height_hint))
    popup_content = MessagePopup(popup_window, message)
    popup_content.btn_close_message_popup.size_hint_x = width_hint
    popup_content.btn_close_message_popup.size_hint_y = None
    popup_content.btn_close_message_popup.height = 50
    popup_window.content = popup_content
    popup_window.open()


class YesNoPopup(NewFloatLayout):
    # question = None
    # popup_window = None
    answer = BooleanProperty(None)

    def __init__(self, popup_window, condition_function, question=None):
        self.question = question
        self.popup_window = popup_window
        self.condition_function = condition_function
        self.app = App.get_running_app()
        super().__init__()

    def set_answer(self, flag):
        self.answer = flag
        self.condition_function(flag)


def show_question_popup(question, condition_function):
    popup_window = ModalView(size_hint=(0.3, 0.3), auto_dismiss=False)
    popup_layout = YesNoPopup(popup_window, condition_function, question)
    popup_window.add_widget(popup_layout)
    popup_window.open()

    return popup_window


class LoadingPopup(NewFloatLayout):
    progress_bar = ObjectProperty(None)
    stage_name = ObjectProperty(None)

    def __init__(self, popup_window, max):
        super(LoadingPopup, self).__init__()

        self.popup_window = popup_window
        self.progress_bar.max = max

    def increment(self):
        self.progress_bar.value += 1
        if self.progress_bar.value == self.progress_bar.max:
            self.popup_window.dismiss()

    def set_stage_name(self, stage_name):
        self.stage_name.text = stage_name

    def set_max(self, max):
        self.progress_bar.max = max


def show_loading_popup(max=1):
    popup_window = ModalView(size_hint=(0.2, 0.1), auto_dismiss=False)
    popup_layout = LoadingPopup(popup_window, max)
    popup_window.add_widget(popup_layout)
    popup_window.open()

    return popup_layout