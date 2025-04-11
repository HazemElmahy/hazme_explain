import subprocess
import sys
import requests
import logging
import webbrowser
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QLabel, QPushButton, QComboBox,
    QDialog, QDialogButtonBox, QGridLayout, QListWidget, QMessageBox, QWidget, QDesktopWidget, QLineEdit
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon  # Import QIcon for setting the window icon
from theme import get_stylesheet  # Import the stylesheet function

# Configure logging
log_file = "./translate_gui.log"
logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

class TranslateGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hazmel Translator")
        self.setGeometry(100, 100, 600, 400)
        self.setWindowIcon(QIcon("../assets/logo.png"))  # Set the app logo
        self.center_window()  # Center the window on the screen
        self.initUI()
        self.apply_stylesheet()  # Apply styles to the UI

    def center_window(self):
        """Center the window on the currently focused screen."""
        screen = QDesktopWidget().screenNumber(QDesktopWidget().cursor().pos())
        screen_geometry = QDesktopWidget().screenGeometry(screen)
        window_geometry = self.frameGeometry()
        center_point = screen_geometry.center()
        window_geometry.moveCenter(center_point)
        self.move(window_geometry.topLeft())

    def initUI(self):
        # Create a central widget and set the layout
        central_widget = QWidget()
        main_layout = QVBoxLayout()  # Main layout for the entire window

        # Display selected text (editable)
        self.selected_text = self.get_clipboard_text()
        if not self.selected_text:
            QMessageBox.critical(self, "Error", "No text selected. Please select some text and try again.")
            logging.error("No text selected. Exiting application.")
            sys.exit(1)

        self.text_input = QLineEdit(self.selected_text)  # Use QLineEdit for editable text
        self.text_input.setObjectName("selectedTextInput")  # Add an object name for styling
        main_layout.addWidget(self.text_input)

        # Create a grid layout for the buttons
        button_layout = QGridLayout()

        # Button size policy
        button_size = 100  # Define a fixed size for the buttons

        # Action buttons
        self.translate_button = QPushButton("Translate")
        self.translate_button.setObjectName("translateButton")
        self.translate_button.setFixedSize(button_size, button_size)  # Set fixed size
        self.translate_button.clicked.connect(self.run_translate)
        button_layout.addWidget(self.translate_button, 0, 0)  # Row 0, Column 0

        self.pronounce_button = QPushButton("Pronounce")
        self.pronounce_button.setObjectName("pronounceButton")
        self.pronounce_button.setFixedSize(button_size, button_size)  # Set fixed size
        self.pronounce_button.clicked.connect(self.run_pronounce)
        button_layout.addWidget(self.pronounce_button, 0, 1)  # Row 0, Column 1

        self.ai_button = QPushButton("AI")
        self.ai_button.setObjectName("aiButton")
        self.ai_button.setFixedSize(button_size, button_size)  # Set fixed size
        self.ai_button.clicked.connect(self.open_ai_dialog)
        button_layout.addWidget(self.ai_button, 0, 2)  # Row 0, Column 2

        self.image_button = QPushButton("Image")
        self.image_button.setObjectName("imageButton")
        self.image_button.setFixedSize(button_size, button_size)  # Set fixed size
        self.image_button.clicked.connect(self.run_image)
        button_layout.addWidget(self.image_button, 0, 3)  # Row 0, Column 3

        # Add the grid layout to the main layout
        main_layout.addLayout(button_layout)

        # Set the layout on the central widget
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def apply_stylesheet(self):
        """Apply the stylesheet from theme.py."""
        self.setStyleSheet(get_stylesheet())

    def get_clipboard_text(self):
        try:
            result = subprocess.run(["xclip", "-o", "-selection", "primary"], stdout=subprocess.PIPE, text=True)
            return result.stdout.strip()
        except Exception as e:
            logging.error(f"Failed to get clipboard text: {e}")
            QMessageBox.critical(self, "Error", f"Failed to get clipboard text: {e}")
            return ""

    def run_translate(self):
        self.call_api(action="translate", text=self.text_input.text())  # Use the updated text

    def run_pronounce(self):
        self.call_api(action="pronounce", text=self.text_input.text())  # Use the updated text

    def run_image(self):
        self.call_api(action="image", text=self.text_input.text())  # Use the updated text

    def open_ai_dialog(self):
        dialog = AIDialog(self.text_input.text(), self)  # Pass the updated text
        if dialog.exec_() == QDialog.Accepted:
            template, model = dialog.get_selection()
            if self.call_api(action="ai", text=self.text_input.text(), template=template, model=model):
                self.close()  # Close the main dialog after the API call is successful

    def call_api(self, action, text, template=None, model=None):
        """Call the FastAPI backend."""
        api_url = "http://127.0.0.1:8000/translate"
        params = {"action": action, "text": text}

        if template:
            params["template"] = template
        if model:
            params["model"] = model

        try:
            logging.info(f"Calling API with params: {params}")
            response = requests.get(api_url, params=params)
            response.raise_for_status()
            data = response.json()
            url = data.get("url")
            if url:
                logging.info(f"API returned URL: {url}")
                # Open the URL in Firefox
                firefox_path = "/usr/bin/firefox"  # Update this path if Firefox is installed elsewhere
                subprocess.run([firefox_path, "-P", "main", url], check=True)
                self.close()  # Close the application after opening Firefox

                return True  # Indicate success
            else:
                logging.warning("No URL returned from the API.")
                QMessageBox.warning(self, "Error", "No URL returned from the API.")
                return False  # Indicate failure
        except requests.RequestException as e:
            logging.error(f"Failed to call API: {e}")
            QMessageBox.critical(self, "Error", f"Failed to call API: {e}")
            return False  # Indicate failure


class AIDialog(QDialog):
    def __init__(self, selected_text, parent=None):
        super().__init__(parent)
        self.setWindowTitle("AI Query Options")
        self.selected_text = selected_text
        self.template = None
        self.model = None
        self.initUI()
        self.apply_stylesheet()  # Apply the theme to the dialog

    def initUI(self):
        layout = QGridLayout()

        # Template selection
        template_label = QLabel("Choose a template:")
        layout.addWidget(template_label, 0, 0)
        self.template_list = QListWidget()
        self.template_list.addItems([
            "1 - Explain this",
            "2 - What does this mean",
            "3 - Translate this in Arabic",
            "4 - Just the selected text"
        ])
        self.template_list.itemDoubleClicked.connect(self.on_template_double_click)
        layout.addWidget(self.template_list, 1, 0, 1, 2)

        # Model selection
        model_label = QLabel("Choose a model:")
        layout.addWidget(model_label, 2, 0)
        self.model_combo = QComboBox()
        self.fetch_models()  # Fetch models from the API
        layout.addWidget(self.model_combo, 3, 0, 1, 2)

        # Dialog buttons
        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        layout.addWidget(self.button_box, 4, 0, 1, 2)

        self.setLayout(layout)

    def fetch_models(self):
        """Fetch available AI models from the API and populate the combo box."""
        api_url = "http://127.0.0.1:8000/models"  # Replace with your API URL
        try:
            response = requests.get(api_url)
            response.raise_for_status()
            data = response.json()
            models = data.get("models", [])
            if models:
                self.model_combo.addItems(models)
            else:
                QMessageBox.warning(self, "Error", "No models available from the API.")
        except requests.RequestException as e:
            logging.error(f"Failed to fetch models from API: {e}")
            QMessageBox.critical(self, "Error", f"Failed to fetch models from API: {e}")

    def apply_stylesheet(self):
        """Apply the stylesheet from theme.py."""
        self.setStyleSheet(get_stylesheet())

    def on_template_double_click(self, item):
        """Handle double-click on a template."""
        self.template = item.text().split(" - ")[0]
        self.model = self.model_combo.currentText()
        self.accept()  # Close the dialog and return QDialog.Accepted

    def get_selection(self):
        """Return the selected template and model."""
        if not self.template:  # If not set by double-click, get the current selection
            self.template = self.template_list.currentItem().text().split(" - ")[0]
        self.model = self.model_combo.currentText()
        return self.template, self.model


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TranslateGUI()
    window.show()
    sys.exit(app.exec_())