from PyQt5.QtWidgets import QLabel

class RQLabel(QLabel):

    def __index__(self, *args):
        super().__init__(*args)