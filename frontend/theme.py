def get_stylesheet():
    """Return the stylesheet for the application."""
    return """
        QMainWindow, QDialog {
            background-color: #121212;
            color: #ffffff;
        }
        QLabel {
            font-size: 14px;
            color: #ffffff;  /* Set text color to white */
        }
        QLineEdit#selectedTextInput, QListWidget {
            font-size: 16px;
            color: #ffffff;
            padding: 10px;
            border: 1px solid #333333;
            border-radius: 5px;
            background-color: #1e1e1e;
        }
        QPushButton {
            font-size: 12px;
            color: #ffffff;
            background-color: #3f51b5;
            border: 2px solid #2c387e;
            border-radius: 5px;
            padding: 5px;
            margin: 5px;
            background: qlineargradient(
                x1: 0, y1: 0, x2: 0, y2: 1,
                stop: 0 #5c6bc0, stop: 1 #3f51b5
            ); /* Gradient for 3D look */
        }
        QPushButton:hover {
            background: qlineargradient(
                x1: 0, y1: 0, x2: 0, y2: 1,
                stop: 0 #7986cb, stop: 1 #5c6bc0
            );
            border: 2px solid #3949ab;
        }
        QPushButton:pressed {
            background: qlineargradient(
                x1: 0, y1: 0, x2: 0, y2: 1,
                stop: 0 #283593, stop: 1 #1a237e
            );
            border: 2px solid #1a237e;
        }
        QComboBox {
            font-size: 14px;
            color: #ffffff;
            background-color: #1e1e1e;
            border: 1px solid #333333;
            border-radius: 5px;
            padding: 5px;
        }
        QComboBox QAbstractItemView {
            background-color: #1e1e1e;
            color: #ffffff;
            selection-background-color: #3f51b5;
        }
        QMessageBox {
            background-color: #1e1e1e;
            color: #ffffff;
        }
    """