from kivy.app import App

from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from WarningPopup import WarningPopup
from kivy.uix.checkbox import CheckBox
from kivy.uix.button import Button

from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout

from random import choice, shuffle
from pyperclip import copy
from string import ascii_lowercase, ascii_uppercase, digits

from time import strftime
from os import environ
from PasswordViewer import PasswordViewer

from openpyxl import load_workbook


class Main(App):
    def __init__(self, **kwargs):
        super(Main, self).__init__(**kwargs)
        self.main_bl = BoxLayout(orientation="vertical")
        self.fields_gl = GridLayout(cols=2, spacing=0)

        self.password_label = Button(text="Your password", on_press=self.copy_password,
                                     font_size=30, background_color=[0, 0, 0, 1], size_hint=(1, 0.5))

        self.password_count_input = TextInput(input_type="number", hint_text="Password length", input_filter="int",
                                              size_hint=(1, 0.1), hint_text_color=[0, 0, 0, 0.8], multiline=False)

        self.password_file_path = "password_file.xlsx"

    def build(self):
        password_fields = [
            "Lower letters",
            "Upper letters",
            "Numbers",
            "Special symbols",
        ]

        for field in password_fields:
            self.fields_gl.add_widget(Label(text=field, size_hint=(2, 1), font_size=30))
            self.fields_gl.add_widget(CheckBox(color=[0, 1, 0, 1], size_hint=(0.2, 4)))

        self.main_bl.add_widget(self.password_count_input)
        self.main_bl.add_widget(self.password_label)

        self.main_bl.add_widget(self.fields_gl)
        self.main_bl.add_widget(Button(text="Generate password", on_press=self.generate_password,
                                       background_color=[0.4, 0.9, 0, 1], size_hint=(1, 0.4)))

        self.main_bl.add_widget(Button(text="Passwords", on_press=self.open_password_file,
                                       background_color=[0.9, 0.2, 0, 1], size_hint=(1, 0.2)))
        return self.main_bl

    def generate_password(self, instance):
        password = []
        fields_list = []
        password_count = 0

        def check_field(field_index, choice_list) -> list:
            try:
                if self.fields_gl.children[field_index].active:
                    return fields_list + [(field_index, choice_list)]

                else:
                    return fields_list

            except Exception as exc:
                print(exc)
                return []

        def add_slice(widget_index, choice_lst, length) -> list:
            try:
                if self.fields_gl.children[widget_index].active:

                    for _ in range(length):
                        password.append(choice(choice_lst))
                return password

            except Exception as exc:
                print(exc, ":", widget_index)

        for index, choice_list in [(6, ascii_lowercase), (4, ascii_uppercase),
                                   (2, digits), (0, r";:'\"&^%$#@!~*&(^)_}{[]\|?>.<=-+_-")]:
            fields_list = check_field(index, choice_list)

        if fields_list == [] or None:
            self.password_label.text = "There is no chosen fields!"
            return
        shuffle(fields_list)

        try:
            password_count = int(self.password_count_input.text)

            if password_count <= 0:
                raise ValueError("Length should be more than zero!")
        except ValueError as exc:
            self.password_count_input.text = ""
            self.password_count_input.background_color = [1, 0.2, 0.2, 0.8]

            if len(str(exc)) > 0:
                self.password_count_input.hint_text = str(exc)

            else:
                self.password_count_input.hint_text = "Undefined error!"
            return

        symbol_add = password_count // len(fields_list)

        while True:
            for index, choice_list in fields_list:
                password = add_slice(index, choice_list, symbol_add)

            if password_count <= len(password):
                password = password[:password_count]
                break

        shuffle(password)
        password = str().join(password)

        self.password_label.text = password
        self.copy_password(instance)

        self.write_password(password)

    def copy_password(self, instance):
        if self.password_label.text != "" or None:
            WarningPopup("Password copied")
            copy(self.password_label.text)

        else:
            WarningPopup("Wrong password, can not copy!")

    def write_password(self, password: str):
        try:
            password_file = load_workbook(self.password_file_path)
            sheet = password_file.active

            sheet.append([strftime("%X:%S"), environ["USERNAME"], password, self.password_count_input.text])
            password_file.save(self.password_file_path)

        except Exception as exc:
            WarningPopup("Error with password file config")
            print(exc)

    def open_password_file(self, instance):
        PasswordViewer(self.password_file_path).open()


if __name__ == '__main__':
    Main().run()
