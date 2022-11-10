import sys

from edit_task import EditTask
from database import TDLdb
from PyQt5.Qt import QBrush
from PyQt5 import QtCore
from PyQt5 import uic
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QMainWindow, QInputDialog, QTableWidgetItem, QMessageBox, QWidget, QHeaderView


class MainWindow(QMainWindow):
    def __init__(self, profile, id):
        super().__init__()
        uic.loadUi('../interfaces/interface_of_to_do_list.ui', self)
        self.add_button.clicked.connect(self.add_list)
        self.edit_button.clicked.connect(self.edit_list)
        self.delete_button.clicked.connect(self.delete_list)
        self.add_task_button.clicked.connect(self.add_task)
        self.completed_button.clicked.connect(self.complete)
        self.edit_task_button.clicked.connect(self.edit_task)
        self.delete_task_button.clicked.connect(self.delete_task)
        self.list_of_lists.currentItemChanged.connect(self.set_tasks)
        self.back_button.clicked.connect(self.back_to_profiles)
        self.profile = profile
        self.database = TDLdb()
        self.profile_id = id
        self.set_lists()
        header = self.table_tasks.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)

    def set_lists(self):
        data = self.database.get_lists(self.profile_id)
        self.list_of_lists.clear()
        for elem in data:
            self.list_of_lists.addItem(elem[-1])

    def set_tasks(self):
        self.list_id = self.database.get_list_id(self.profile_id, self.list_of_lists.currentItem().text())
        data = self.database.get_tasks(self.list_id)
        self.table_tasks.clear()
        self.table_tasks.setRowCount(len(data))
        self.table_tasks.setColumnCount(2)
        header = self.table_tasks.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        titles = ['Задание', 'Состояние']
        for i, elem in enumerate(titles):
            self.table_tasks.setHorizontalHeaderItem(i, QTableWidgetItem(str(elem)))
        for i, elem in enumerate(data):
            for j, val in enumerate(elem):
                item = QTableWidgetItem(str(val))
                item.setFlags(QtCore.Qt.ItemIsEnabled)
                self.table_tasks.setItem(i, j, item)

    def add_list(self):
        name, ok_pressed = QInputDialog.getText(self, 'Введите название листа',
                                                'Введите название листа')
        if ok_pressed:
            self.database.add_lists(self.profile_id, name)
        self.set_lists()

    def add_task(self):
        name, ok_pressed = QInputDialog.getText(self, 'Новое задание',
                                                'Введите ваше задание')
        if ok_pressed:
            self.database.add_task(self.list_id, name)
        self.set_tasks()

    def edit_list(self):
        id = self.database.get_list_id(self.profile_id, self.list_of_lists.currentItem().text())
        name, ok_pressed = QInputDialog.getText(self, 'Редактирование',
                                                'Введите новое название')
        if ok_pressed:
            self.database.edit_list(id, name)
        self.set_lists()

    def edit_task(self):
        text = self.table_tasks.currentItem().text()
        task_id = self.database.get_task_id(text)
        state = self.database.get_state_task(task_id)
        self.edit_task_app = EditTask(self, self.list_id, task_id, text, state)
        self.edit_task_app.show()

    def delete_list(self):
        self.database.delete_list(self.list_id)
        self.set_lists()

    def delete_task(self):
        key = QMessageBox.question(self, 'Подтверждение',
                                   'Вы уверены, что хотете удалить задание?')
        if key == QMessageBox.Yes:
            text = self.table_tasks.currentItem().text()
            task_id = self.database.get_task_id(text)
            self.database.delete_task(task_id)
            self.set_tasks()

    def complete(self):
        text = self.table_tasks.currentItem().text()
        task_id = self.database.get_task_id(text)
        self.database.complete_task(task_id)
        self.set_tasks()

    def back_to_profiles(self):
        self.profile.show()
        self.database.close_connection()
        self.close()
