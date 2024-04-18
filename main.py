#!/usr/bin/env python

import sys, os
import ui.resource_ui
from PyQt5 import uic, QtGui, QtCore
from PyQt5.QtWidgets import (
    QMainWindow,
    QApplication,
    QDialog,
    QListWidgetItem,
    QFileDialog,
)

from wad import unwad


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi("ui/main.ui", self)

        self.wad_path = None
        self.texture_size = 128
        self.texture_spacing = 17

        self.show()

        # disabling some actions (for now)
        self.disable_actions([self.actionView_Animated, self.actionView_Detailed])

        # connections
        self.actionAbout.triggered.connect(lambda: AboutWindow().exec_())
        self.actionOpen.triggered.connect(lambda: self.open_wad())
        self.actionZoom_In.triggered.connect(lambda: self.adjust_zoom("in"))
        self.actionZoom_Out.triggered.connect(lambda: self.adjust_zoom("out"))
        self.actionDelete.triggered.connect(lambda: self.delete_textures())
        self.actionSelect_All.triggered.connect(lambda: self.select_all())
        self.actionDeselect_All.triggered.connect(lambda: self.deselect_all())

        if not self.wad_path:
            self.setWindowTitle("Untitled - Qt WADitor")

    def adjust_zoom(self, zoom_type):
        if zoom_type == "in" and self.texture_size < 128:
            self.texture_size += 16
        elif zoom_type == "out" and self.texture_size > 16:
            self.texture_size -= 16
        else:
            return

        self.lw_textures.setIconSize(QtCore.QSize(self.texture_size, self.texture_size))

    def open_wad(self):
        try:
            self.wad_path, _ = QFileDialog.getOpenFileName(
                self, "Select a WAD file", "", "WAD Files (*.wad);;All Files (*)"
            )

            self.unpack_wad(self.wad_path)
            self.setWindowTitle(f"{os.path.basename(self.wad_path)} - Qt WADitor")

        except Exception as e:
            print(f"[open_wad] {e}")

    def unpack_wad(self, path):
        unwadded = unwad(path)
        temp_dir = unwadded[0]
        textures = unwadded[1]

        self.lw_textures.clear()
        for t in textures:
            scaled_pixmap = QtGui.QPixmap(f"{temp_dir}/{t}").scaled(
                self.texture_size, self.texture_size, QtCore.Qt.KeepAspectRatio
            )

            scaled_icon = QtGui.QIcon(scaled_pixmap)

            item = QListWidgetItem(scaled_icon, str(t))
            item.setData(QtCore.Qt.UserRole, f"{temp_dir}/{t}")
            print(QtCore.Qt.UserRole)
            self.lw_textures.addItem(item)

    def disable_actions(self, actions):
        self.actionView_Animated.setEnabled(False)
        self.actionView_Detailed.setEnabled(False)

        for a in actions:
            if not a.isEnabled():
                tooltip = a.toolTip() + " [DISABLED]"
                a.setToolTip(tooltip)

    def delete_textures(self):
        print("we deleting stuff")
        textures = self.lw_textures.selectedItems()
        for t in textures:
            self.lw_textures.takeItem(self.lw_textures.row(t))
            # print(t.text())
            # print(t.data(QtCore.Qt.UserRole))

    def select_all(self):
        for i in range(self.lw_textures.count()):
            self.lw_textures.item(i).setSelected(True)

    def deselect_all(self):
        for i in range(self.lw_textures.count()):
            self.lw_textures.item(i).setSelected(False)


class AboutWindow(QDialog):
    def __init__(self):
        super(AboutWindow, self).__init__()
        uic.loadUi("ui/about.ui", self)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    UIWindow = MainWindow()
    app.exec_()
