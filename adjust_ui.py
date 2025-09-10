# This one is extremely unfinished, trying to extract parts into scripts to work on

from PyQt5.QtWidgets import (
        QApplication, QSpinBox, QDoubleSpinBox, QToolBar,
        QSlider, QComboBox, QWidget, QDockWidget, QToolButton,
        QAbstractSlider, QLabel, QRadioButton, QLineEdit,
        QTreeView, QHeaderView, QStyledItemDelegate, QAbstractButton # Added QTreeView and QHeaderView
        )
from PyQt5.QtCore import QSize
import sys

# ==============================================================================
#                               CONFIGURATION
# ==============================================================================

# Global Settings for common UI elements
GLOBAL_TOOLBAR_ICON_SIZE = QSize(25, 25)
GLOBAL_TOOLBAR_FIXED_HEIGHT = 27
GLOBAL_SPINBOX_FIXED_HEIGHT = 18
GLOBAL_SPINBOX_FIXED_WIDTH = 18

# Layers Docker (KisLayerBox) Settings
LAYERS_DOCKER_OBJECT_NAME = "KisLayerBox"
LAYERS_COMBOBOX_FIXED_HEIGHT = 18
LAYERS_COMBOBOX_FIXED_WIDTH= 150 
LAYERS_TOOLBUTTON_ICON_SIZE = QSize(16, 16) # For buttons like Add, Delete, Duplicate etc.
LAYERS_TOOLBUTTON_FIXED_HEIGHT = 20 # Optional: Set a fixed height for these buttons (set to 0 to disable)

# Layer List (QTreeView) specific settings
#LAYERS_LIST_ROW_HEIGHT = 18 # Adjust the height of each layer entry in the list
#LAYERS_LIST_ROW_WIDTH = 18 # Adjust the height of each layer entry in the list
#HIDE_LAYER_THUMBNAILS = True # Set to True to attempt hiding layer thumbnails

# --- Hide Docker Title Bar Elements ---
# This attempts to hide the entire title bar area of the dockers.
# Be aware: This might make it harder to drag/undock the panels if they don't have alternative handles.
HIDE_LAYERS_DOCKER_TITLE_BAR = False

# ==============================================================================
#                            END OF CONFIGURATION
# ==============================================================================

def is_descendant_of(potential_child, potential_parent):
    """
    Recursively checks if potential_child is a direct or indirect child of potential_parent.
    """
    current_parent = potential_child.parent()
    while current_parent is not None:
        if current_parent is potential_parent:
            return True
        current_parent = current_parent.parent()
    return False

# --- GLOBAL ADJUSTMENTS ---
for widget in QApplication.allWidgets():
    # Adjust ToolBar icon size and height globally
    if isinstance(widget, QToolBar):
        widget.setIconSize(GLOBAL_TOOLBAR_ICON_SIZE)
        widget.setFixedHeight(GLOBAL_TOOLBAR_FIXED_HEIGHT)

    # Adjust SpinBox/DoubleSpinBox height globally
    if isinstance(widget, (QSpinBox, QDoubleSpinBox)):
        widget.setFixedHeight(GLOBAL_SPINBOX_FIXED_HEIGHT)
        #widget.setFixedWidth(GLOBAL_SPINBOX_FIXED_WIDTH)

# --- Find the specific docker ---
layers_docker = None
for widget in QApplication.allWidgets():
    if isinstance(widget, QDockWidget):
        if widget.objectName() == LAYERS_DOCKER_OBJECT_NAME:
            layers_docker = widget
            break

print(f"Layers Docker Found: {layers_docker is not None}")

# --- Targeted Adjustments within found docker ---
if layers_docker:
    for widget in QApplication.allWidgets():
        # --- Hide Docker Title Bar ---
        if HIDE_LAYERS_DOCKER_TITLE_BAR and widget is layers_docker:
            # Hide title bar buttons and title bar if possible
            for child_of_docker in widget.children():
                if isinstance(child_of_docker, QAbstractButton) and child_of_docker.objectName() in ['qt_dockwidget_floatbutton', 'qt_dockwidget_closebutton']:
                    child_of_docker.hide()
                    child_of_docker.setFixedSize(0,0)
                    print(f"Hidden title bar button: {child_of_docker.objectName()}")
                if isinstance(child_of_docker, QWidget) and child_of_docker.objectName() == 'qt_dockwidget_titlebar':
                    print(f"Hiding docker title bar for {widget.objectName()}")
                    child_of_docker.hide()
                    child_of_docker.setFixedSize(0,0)
                    break # Found and hid the title bar, move on

        # --- Layers Docker Adjustments ---
        if layers_docker and is_descendant_of(widget, layers_docker):
            # Adjust QComboBox height (for blend mode - 'cmbComposite')
            if isinstance(widget, QComboBox):
                print(f"Adjusting QComboBox in Layers Docker: {widget.objectName() or widget.__class__.__name__}")
                widget.setFixedHeight(LAYERS_COMBOBOX_FIXED_HEIGHT)
                #widget.setFixedWidth(LAYERS_COMBOBOX_FIXED_WIDTH)

            # Adjust QToolButton icon size and height for layer action buttons
            if isinstance(widget, QToolButton) and widget.objectName() in [
                    'bnAdd', 'bnDuplicate', 'bnLower', 'bnRaise', 'bnProperties', 'bnDelete', 'bnLayerFilters'
                    ]:
                print(f"Adjusting QToolButton icon in Layers Docker: {widget.objectName()}")
                widget.setIconSize(LAYERS_TOOLBUTTON_ICON_SIZE)
                # Apply fixed height if configured (and not 0)
                if LAYERS_TOOLBUTTON_FIXED_HEIGHT > 0:
                    widget.setFixedHeight(LAYERS_TOOLBUTTON_FIXED_HEIGHT)

else:
    print("Warning: Layers docker was not found. Check object name.")
