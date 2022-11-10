import sys

from database import TDLdb
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow


class EditTask(QMainWindow):
    def __init__(self, widget, list_id, task_id, text, state):
        super().__init__()
        uic.loadUi('../interfaces/interface_of_edit_task.ui', self)
        self.cancel_button.clicked.connect(self.close_app)
        self.confirm_button.clicked.connect(self.edit_task)
        self.database = TDLdb()
        self.widget = widget
        self.list_id = list_id
        self.task_id = task_id
        self.text = text
        self.state = state
        self.set_window()

    def set_window(self):
        self.text_inp.setText(self.text)
        if self.state == 'Выполнено':
            self.state_chs.setCurrentIndex(0)
        else:
            self.state_chs.setCurrentIndex(1)

    def edit_task(self):
        text = self.text_inp.text()
        state = self.state_chs.currentText()
        self.database.edit_task(self.task_id, text, state)
        self.widget.set_tasks()
        self.close()

    def close_app(self):
        self.database.close_connection()
        self.close()
