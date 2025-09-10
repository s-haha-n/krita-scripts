from PyQt5.QtWidgets import (
    QApplication, QComboBox, QWidget, QDockWidget, QToolButton,
    QAbstractSlider, QLabel, QRadioButton, QLineEdit
)
from PyQt5.QtCore import QSize, Qt

# ==============================================================================
#                               CONFIGURATION
# ==============================================================================

COLOR_SELECTOR_DOCKER_OBJECT_NAME = "SpecificColorSelector"
COLOR_SLIDER_FIXED_HEIGHT = 12
COLOR_SELECTOR_COMBOBOX_FIXED_HEIGHT = 40

HIDE_COLOR_SELECTOR_COLOR_MODEL_DROPDOWN = True
HIDE_COLOR_SELECTOR_RADIO_BUTTONS = True
HIDE_COLOR_SELECTOR_COLOR_NAME_SECTION = True

# ==============================================================================
#                            END OF CONFIGURATION
# ==============================================================================

def is_descendant_of(potential_child, potential_parent):
    current_parent = potential_child.parent()
    while current_parent is not None:
        if current_parent is potential_parent:
            return True
        current_parent = current_parent.parent()
    return False

# --- Find the specific color selector docker ---
color_selector_docker = None
for widget in QApplication.allWidgets():
    if isinstance(widget, QDockWidget) and widget.objectName() == COLOR_SELECTOR_DOCKER_OBJECT_NAME:
        color_selector_docker = widget
        break

print(f"Specific Color Selector Docker Found: {color_selector_docker is not None}")

# --- Targeted Adjustments within found docker ---
if color_selector_docker:

    main_widget = color_selector_docker.widget()
    if main_widget:
        children = [w for w in main_widget.findChildren(QWidget, options=Qt.FindDirectChildrenOnly)]
        if children:
            first_child = children[0]
            second_child = children[1]
            print(f"Hiding first child widget: {first_child.__class__.__name__}")
            first_child.hide()
            second_child.hide() # just hid the first two elements couldn't figure this out, if the first two elements change in an update this should too
            first_child.setFixedSize(0, 0)

    for widget in QApplication.allWidgets():
        if is_descendant_of(widget, color_selector_docker):
            # Adjust QAbstractSlider height (for the actual color sliders: H, S, V, R, G, B)
            if isinstance(widget, QAbstractSlider):
                print(f"Adjusting QAbstractSlider in Specific Color Selector Docker: {widget.objectName() or widget.__class__.__name__}")
                widget.setFixedHeight(COLOR_SLIDER_FIXED_HEIGHT)

            # Adjust QComboBox height (for HSV/RGB color model dropdown)
            if isinstance(widget, QComboBox) and not widget.objectName():
                print(f"Adjusting QComboBox in Specific Color Selector Docker: {widget.objectName() or widget.__class__.__name__}")
                if HIDE_COLOR_SELECTOR_COLOR_MODEL_DROPDOWN:
                    widget.hide()
                    widget.setFixedSize(0,0)
                else:
                    widget.setFixedHeight(COLOR_SELECTOR_COMBOBOX_FIXED_HEIGHT)

            # Hide Radio Buttons (QRadioButton)
            if HIDE_COLOR_SELECTOR_RADIO_BUTTONS and isinstance(widget, QRadioButton):
                print(f"Hiding QRadioButton in Specific Color Selector: {widget.objectName() or widget.__class__.__name__}")
                widget.hide()
                widget.setFixedSize(0,0)

            # "Color name:" label and its QLineEdit
            if HIDE_COLOR_SELECTOR_COLOR_NAME_SECTION:
                if isinstance(widget, QLabel) and widget.text() == 'Color name:':
                    parent_of_label = widget.parent()
                    if isinstance(parent_of_label, QWidget) and not parent_of_label.objectName():
                        print(f"Hiding Color name section parent widget: {parent_of_label.__class__.__name__}")
                        parent_of_label.hide()
                        parent_of_label.setFixedSize(0,0)
                elif isinstance(widget, QLineEdit) and not widget.objectName():
                    print(f"Hiding QLineEdit in Color Selector (no obj name): {widget.__class__.__name__}")
                    widget.hide()
                    widget.setFixedSize(0,0)
else:
    print("Warning: Specific Color Selector Docker was not found. Check the object name.")
