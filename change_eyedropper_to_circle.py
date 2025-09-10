from krita import Krita
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QCursor, QPixmap, QPainter, QColor
from PyQt5.QtCore import Qt, QObject, QEvent

app = QApplication.instance()

def make_circle_cursor(radius_px=12, color=QColor("purple")):
    size = radius_px * 2 + 4
    pixmap = QPixmap(size, size)
    pixmap.fill(Qt.transparent)
    p = QPainter(pixmap)
    p.setRenderHint(QPainter.Antialiasing)
    p.setPen(color)
    p.drawEllipse(2, 2, radius_px*2, radius_px*2)
    p.end()
    return QCursor(pixmap, radius_px+2, radius_px+2)

class PickerCursorFilter(QObject):
    def __init__(self):
        super().__init__()
        self.active = False

    def eventFilter(self, obj, event):
        if event.type() == QEvent.KeyPress and event.key() in (Qt.Key_Enter, Qt.Key_Return):
            if not self.active:
                self.active = True
                radius = self.get_picker_radius()
                QApplication.setOverrideCursor(make_circle_cursor(radius))
        elif event.type() == QEvent.KeyRelease and event.key() in (Qt.Key_Enter, Qt.Key_Return):
            if self.active:
                self.active = False
                QApplication.restoreOverrideCursor()
        return False

    def get_picker_radius(self):
        try:
            krita = Krita.instance()
            win = krita.activeWindow()
            view = win.activeView() if win else None
            if view and view.toolName() == "KisToolColorPicker":
                # Read "radius" option from the Color Picker tool
                r = view.toolOption("radius")
                return max(4, int(r))  # fall back if too small
        except Exception:
            pass
        return 12  # default fallback

# remove old filter if re-running
if hasattr(app, "_picker_filter"):
    app.removeEventFilter(app._picker_filter)

filt = PickerCursorFilter()
app.installEventFilter(filt)
app._picker_filter = filt

print("Custom color picker circle cursor active. Press Numpad Enter to see it.")

