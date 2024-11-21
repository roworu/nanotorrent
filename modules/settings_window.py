from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFileDialog,
    QTabWidget, QWidget, QSpinBox, QHBoxLayout, QComboBox
)


class SettingsWindow(QDialog):
    def __init__(self, parent=None, settings_handler=None):
        super().__init__(parent)

        self.setWindowTitle("Settings")
        self.setGeometry(200, 200, 400, 300)

        # Reference to the settings handler
        self.settings_handler = settings_handler

        # Tabbed layout
        self.layout = QVBoxLayout()
        self.tabs = QTabWidget()
        self.layout.addWidget(self.tabs)

        # Downloads Tab
        self.downloads_tab = QWidget()
        self.setup_downloads_tab()
        self.tabs.addTab(self.downloads_tab, "Downloads")

        # Speed Settings Tab
        self.speed_tab = QWidget()
        self.setup_speed_tab()
        self.tabs.addTab(self.speed_tab, "Speed")

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

    def setup_speed_tab(self):
        """Setup the Speed tab."""
        speed_layout = QVBoxLayout()

        # Max Download Speed
        self.max_download_label = QLabel("Max Download Speed:")
        speed_layout.addWidget(self.max_download_label)

        download_layout = QHBoxLayout()
        self.max_download_spinbox = QSpinBox(self)
        self.max_download_spinbox.setRange(0, 10_000_000)  # 0 means unlimited
        download_layout.addWidget(self.max_download_spinbox)

        self.download_unit_selector = QComboBox(self)
        self.download_unit_selector.addItems(["kB/s", "MB/s"])
        download_layout.addWidget(self.download_unit_selector)

        speed_layout.addLayout(download_layout)

        # Max Upload Speed
        self.max_upload_label = QLabel("Max Upload Speed:")
        speed_layout.addWidget(self.max_upload_label)

        upload_layout = QHBoxLayout()
        self.max_upload_spinbox = QSpinBox(self)
        self.max_upload_spinbox.setRange(0, 10_000_000)  # 0 means unlimited
        upload_layout.addWidget(self.max_upload_spinbox)

        self.upload_unit_selector = QComboBox(self)
        self.upload_unit_selector.addItems(["kB/s", "MB/s"])
        upload_layout.addWidget(self.upload_unit_selector)

        speed_layout.addLayout(upload_layout)

        self.speed_tab.setLayout(speed_layout)

    def browse_path(self):
        """Open a dialog to select a download path."""
        path = QFileDialog.getExistingDirectory(self, "Select Download Directory")
        if path:
            self.download_path_edit.setText(path)

    def load_settings(self):
        """Load settings from the settings handler."""
        download_path = self.settings_handler.get("Downloads", "download_path")
        self.download_path_edit.setText(download_path)

        # Load download speed
        max_download_speed = int(self.settings_handler.get("Speed", "max_download_speed"))
        if max_download_speed >= 1_000_000:
            self.max_download_spinbox.setValue(max_download_speed // 1_000_000)
            self.download_unit_selector.setCurrentText("MB/s")
        else:
            self.max_download_spinbox.setValue(max_download_speed // 1_000)
            self.download_unit_selector.setCurrentText("kB/s")

        # Load upload speed
        max_upload_speed = int(self.settings_handler.get("Speed", "max_upload_speed"))
        if max_upload_speed >= 1_000_000:
            self.max_upload_spinbox.setValue(max_upload_speed // 1_000_000)
            self.upload_unit_selector.setCurrentText("MB/s")
        else:
            self.max_upload_spinbox.setValue(max_upload_speed // 1_000)
            self.upload_unit_selector.setCurrentText("kB/s")

    def save_settings(self):
        """Save the settings to the settings handler."""
        download_path = self.download_path_edit.text()
        self.settings_handler.set("Downloads", "download_path", download_path)

        # Save download speed
        max_download_speed = self.max_download_spinbox.value()
        if self.download_unit_selector.currentText() == "MB/s":
            max_download_speed *= 1_000_000  # Convert MB/s to bytes/s
        else:
            max_download_speed *= 1_000  # Convert kB/s to bytes/s
        self.settings_handler.set("Speed", "max_download_speed", str(max_download_speed))

        # Save upload speed
        max_upload_speed = self.max_upload_spinbox.value()
        if self.upload_unit_selector.currentText() == "MB/s":
            max_upload_speed *= 1_000_000  # Convert MB/s to bytes/s
        else:
            max_upload_speed *= 1_000  # Convert kB/s to bytes/s
        self.settings_handler.set("Speed", "max_upload_speed", str(max_upload_speed))

        self.accept()
