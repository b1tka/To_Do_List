import sys

from main_window import MainWindow
from database import TDLdb
from Exceptions import NotSelected
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QInputDialog, QMessageBox


class ChooseYourProfile(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('../interfaces/interface_of_profiles.ui', self)
        self.choose_button.clicked.connect(self.choose_profile)
        self.create_button.clicked.connect(self.add_new_profile)
        self.delete_button.clicked.connect(self.delete_profile)
        self.database = TDLdb()
        self.set_table()

    def set_table(self):
        profiles = self.database.get_profiles()
        self.profiles_list.clear()
        for elem in profiles:
            self.profiles_list.addItem(elem[-1])

    def add_new_profile(self):
        name, ok_pressed = QInputDialog.getText(self, 'Введите название профиля',
                                                'Введите название профиля')
        if ok_pressed:
            self.database.add_profiles(name)
        self.set_table()

    def choose_profile(self):
        try:
            if not self.profiles_list.selectedItems():
                raise NotSelected
            name = self.profiles_list.currentItem().text()
            id = self.database.get_id(name)[0]
            self.main_window = MainWindow(self, id)
            self.main_window.show()
            self.hide()
        except NotSelected:
            QMessageBox.critical(self, 'Error', 'Выберите профиль', QMessageBox.Ok)

    def delete_profile(self):
        name = self.profiles_list.currentItem().text()
        id = self.database.get_id(name)[0]
        self.database.delete_profile(id)
        self.set_table()

    def close_app(self):
        self.close()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ChooseYourProfile()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec_())
