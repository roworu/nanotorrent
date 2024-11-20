from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFileDialog,
    QTabWidget, QWidget
)
import logging
from modules.utils.settings_handler import SettingsHandler


class SettingsWindow(QDialog):
    def __init__(self, parent=None, settings_handler=None):
        super().__init__(parent)

        self.setWindowTitle("Settings")
        self.setGeometry(200, 200, 400, 300)

        # Reference to the settings handler
        self.settings_handler = settings_handler or SettingsHandler("settings.ini")

        # Tabbed layout
        self.layout = QVBoxLayout()
        self.tabs = QTabWidget()
        self.layout.addWidget(self.tabs)

        # Downloads Tab
        self.downloads_tab = QWidget()
        self.setup_downloads_tab()
        self.tabs.addTab(self.downloads_tab, "Downloads")

        # Save Button
        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save_settings)
        self.layout.addWidget(self.save_button)

        self.setLayout(self.layout)

        # Load settings on initialization
        self.load_settings()

    def setup_downloads_tab(self):
        """Setup the Downloads tab."""
        downloads_layout = QVBoxLayout()

        # Download Path
        self.download_path_label = QLabel("Download Path:")
        downloads_layout.addWidget(self.download_path_label)

        self.download_path_edit = QLineEdit(self)
        downloads_layout.addWidget(self.download_path_edit)

        self.select_path_button = QPushButton("Browse")
        self.select_path_button.clicked.connect(self.browse_path)
        downloads_layout.addWidget(self.select_path_button)

        self.downloads_tab.setLayout(downloads_layout)

    def browse_path(self):
        """Open a dialog to select a download path."""
        path = QFileDialog.getExistingDirectory(self, "Select Download Directory")
        if path:
            self.download_path_edit.setText(path)

    def load_settings(self):
        """Load settings from the settings handler."""
        download_path = self.settings_handler.get("Downloads", "download_path")
        self.download_path_edit.setText(download_path)
        logging.info("Settings loaded")

    def save_settings(self):
        """Save the settings to the settings handler."""
        download_path = self.download_path_edit.text()
        self.settings_handler.set("Downloads", "download_path", download_path)

        logging.info(f"Settings saved: download_path={download_path}")
        self.accept()

    def get_download_path(self):
        """Return the current download path."""
        return self.download_path_edit.text()
