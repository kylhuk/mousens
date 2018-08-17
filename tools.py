import ctypes


class MessageBox:

    def show(self, title, text, style):
        ctypes.windll.user32.MessageBoxW(0, text, title, style)

