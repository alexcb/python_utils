#!/usr/bin/env python2.7

import os
import json
import time

from pprint import pprint

from PyQt5.QtCore import QFile, QIODevice, Qt, QTextStream, QStringListModel, QAbstractListModel, QModelIndex, pyqtSignal
from PyQt5.QtWidgets import (QDialog, QFileDialog, QGridLayout, QHBoxLayout,
        QLabel, QLineEdit, QMessageBox, QPushButton, QTextEdit, QVBoxLayout,
        QWidget, QListView)

task_path = os.path.expanduser("~/.alex_tasks")

class MyQListView(QListView):
    itemDropped = pyqtSignal()

    def __init__(self, parent=None):
        super(MyQListView, self).__init__(parent)

    def dropEvent(self, event):
        super(MyQListView, self).dropEvent(event)
        self.itemDropped.emit()

    def rowsAboutToBeRemoved(self, parent, start, end):
        super(MyQListView, self).rowsAboutToBeRemoved(parent, start, end)

    def dragLeaveEvent(self, event):
        super(MyQListView, self).dragLeaveEvent(event)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Delete:
            for item in self.selectedIndexes():
                self.model().removeRows(item.row(), 1)
            self.clearSelection()
            return
        return super(MyQListView, self).keyPressEvent(event)

    def focusOutEvent(self, event):
        self.clearSelection()



class MyQStringListModel(QStringListModel):
    itemAdded = pyqtSignal()
    itemRemoved = pyqtSignal()
    def __init__(self, items, parent=None):
        super(MyQStringListModel, self).__init__(items, parent)

    def flags(self, index):
        if index.isValid():
             return Qt.ItemIsDragEnabled | Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsEditable
        return Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsDropEnabled

    def insertRows(self, *args):
        res = super(MyQStringListModel, self).insertRows(*args)
        self.itemAdded.emit()
        return res

    def removeRows(self, *args):
        res = super(MyQStringListModel, self).removeRows(*args)
        self.itemRemoved.emit()
        return res


class TaskManager(QWidget):

    def __init__(self, parent=None):
        super(TaskManager, self).__init__(parent)

        nameLabel = QLabel("Name:")

        self._new_task = QLineEdit()
        self._new_task.returnPressed.connect(self.addTask)

        self.today_model = MyQStringListModel([], self)
        self.tomorrow_model = MyQStringListModel([], self)
        self.loadTasks()

        self.today_model.itemAdded.connect(self.saveTasks)
        self.tomorrow_model.itemAdded.connect(self.saveTasks)
        self.today_model.itemRemoved.connect(self.saveTasks)
        self.tomorrow_model.itemRemoved.connect(self.saveTasks)
        self.today_model.dataChanged.connect(self.saveTasks)
        self.tomorrow_model.dataChanged.connect(self.saveTasks)

        today_view = MyQListView()
        today_view.setModel(self.today_model)
        today_view.setDragEnabled(True)
        today_view.setAcceptDrops(True)
        today_view.setDefaultDropAction(Qt.MoveAction)
        pprint([x for x in dir(today_view) if 'key' in x.lower()])

        tomorrow_view = MyQListView()
        tomorrow_view.setModel(self.tomorrow_model)
        tomorrow_view.setDragEnabled(True)
        tomorrow_view.setAcceptDrops(True)
        tomorrow_view.setDefaultDropAction(Qt.MoveAction)
        tomorrow_view.itemDropped.connect(self.saveTasks)

        mainLayout = QGridLayout()
        mainLayout.addWidget(self._new_task, 0, 0)
        mainLayout.addWidget(today_view, 1, 0)
        mainLayout.addWidget(tomorrow_view, 1, 1)

        self.setLayout(mainLayout)
        self.setWindowTitle("Alex's Task")

    def keypress(self, event):
        print event

    def addTask(self):
        tasks = self.today_model.stringList()
        tasks.append(self._new_task.text())
        self._new_task.clear()

        self.today_model.setStringList(tasks)
        self.saveTasks()

    def saveTasks(self):
        print 'save'
        with open(task_path, "w") as fp:
            fp.write(json.dumps({
                "tasks": {
                    "today": self.today_model.stringList(),
                    "tomorrow": self.tomorrow_model.stringList(),
                    },
                "time": time.time(),
                "version": 1,
                }))

    def loadTasks(self):
        try:
            with open(task_path, "r") as fp:
                tasks = json.load(fp)

            self.today_model.setStringList(tasks['tasks']['today'])
            self.tomorrow_model.setStringList(tasks['tasks']['tomorrow'])
        except:
            pass




if __name__ == '__main__':
    import sys

    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)

    tm = TaskManager()
    tm.show()

    sys.exit(app.exec_())
