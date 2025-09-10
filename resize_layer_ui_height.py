# THIS ALSO MESSES UP ALL ICONS
# and makes the layer thumbnail preview go away in combo with other scripts
# not sure why...

from PyQt5.QtWidgets import QApplication, QTreeView, QStyledItemDelegate, QStyleOptionViewItem
from PyQt5.QtCore import QSize

class SizeHintProxy(QStyledItemDelegate):
    def __init__(self, base_delegate, row_height=20, icon_size=16):
        super().__init__(base_delegate.parent())
        self.base = base_delegate
        self.row_height = row_height
        #self.icon_size = icon_size

    def paint(self, painter, option, index):
        # forward painting to the original delegate if possible
        if hasattr(self.base, "paint"):
            self.base.paint(painter, option, index)
        else:
            super().paint(painter, option, index)

    def sizeHint(self, option, index):
        opt = QStyleOptionViewItem(option)
        #opt.decorationSize = QSize(self.icon_size, self.icon_size)
        if hasattr(self.base, "sizeHint"):
            size = self.base.sizeHint(opt, index)
        else:
            size = super().sizeHint(opt, index)
        size.setHeight(self.row_height)
        return size

# apply proxy
for widget in QApplication.allWidgets():
    if isinstance(widget, QTreeView) and widget.objectName() == 'listLayers':
        current = widget.itemDelegate()
        widget.setIconSize(QSize(16, 16))   # adjust to taste
        proxy = SizeHintProxy(current, row_height=18, icon_size=64)
        widget.setItemDelegate(proxy)
        widget.viewport().update()
