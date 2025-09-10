from PyQt5.QtWidgets import QApplication, QTreeView, QHeaderView

from PyQt5.QtWidgets import ( QApplication, QTreeView )

from PyQt5.QtCore import QSize

import sys

WIDTH = 205 

# Find the Layers Docker's QTreeView (usually named 'listLayers')
for widget in QApplication.allWidgets():
      if isinstance(widget, QTreeView) and widget.objectName() == 'listLayers':
          widget.setFixedWidth(WIDTH)
