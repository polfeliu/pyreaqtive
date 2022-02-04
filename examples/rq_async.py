import sys

import requests
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget

from pyreaqtive import RQList, RQCombobox, RQChoice, RQAsync, RQComputedList


def get_authors():
    res = requests.get(f"https://poetrydb.org/authors")
    return [Author(name) for name in res.json()['authors']]


class Author:

    def __init__(self, name):
        self.name = name

    def get_author_titles(self):
        res = requests.get(f"https://poetrydb.org/author/{self.name}/title")
        return [Title(title['title']) for title in res.json()]

    def __str__(self):
        return self.name


class Title:

    def __init__(self, name):
        self.name = name

    def get_text(self):
        res = requests.get(f"https://poetrydb.org/title/{self.name}/lines")
        return res.json()  # TODO

    def __str__(self):
        return self.name


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        widget = QWidget()
        layout = QVBoxLayout()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        self.author_list = RQList()
        self.get_author_list = RQAsync(
            task=lambda: self.author_list.set(get_authors()),
            trigger=RQAsync.AutoTriggers.Start
        )

        self.author_selected = RQChoice(self.author_list, allow_none=True)

        self.author_select = RQCombobox(self.author_selected, rq_disabled=self.get_author_list.working)
        layout.addWidget(self.author_select)

        self.title_list = RQList()

        self.get_title_list = RQAsync(
            task=lambda: self.title_list.set(
                self.author_selected.get().get_author_titles()) if self.author_selected.get() is not None else None,
            trigger=self.author_selected

        )

        self.title_selected = RQChoice(self.title_list, allow_none=True)

        self.title_select = RQCombobox(self.title_selected)
        layout.addWidget(self.title_select)


app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
