import configparser
import os


class SettingsHandler:
    def __init__(self, file_name):
        self.file_name = file_name
        self.config = configparser.ConfigParser()

        # Ensure the settings file exists
        if not os.path.exists(self.file_name):
            self._create_default_settings()
        else:
            self._load_settings()

    def _create_default_settings(self):
        """Create default settings and save them to the file."""
        self.config["Downloads"] = {"download_path": ""}
        self.config["UI"] = {"theme": "Light"}
        self.save()

    def _load_settings(self):
        """Load settings from the file, ensuring all sections and options exist."""
        try:
            self.config.read(self.file_name)

            # Validate and add missing sections or options
            if "Downloads" not in self.config:
                self.config["Downloads"] = {"download_path": ""}
            if "UI" not in self.config:
                self.config["UI"] = {"theme": "Light"}
            self.save()  # Save updated settings if any defaults were added
        except configparser.Error as e:
            print(f"Error loading configuration file: {e}")
            self._create_default_settings()

    def get(self, section, option):
        """
        Get a value from the settings file.
        If the section or option is missing, return an empty string and add it to the file.
        """
        try:
            value = self.config.get(section, option)
            return value
        except (configparser.NoSectionError, configparser.NoOptionError):
            # Add missing section/option with default value
            self.set(section, option, "")
            return ""

    def set(self, section, option, value):
        """Set a value in the settings file."""
        if section not in self.config:
            self.config[section] = {}
        self.config[section][option] = value
        self.save()

    def save(self):
        """Save the current settings to the file."""
        try:
            with open(self.file_name, "w") as f:
                self.config.write(f)
        except OSError as e:
            print(f"Error saving configuration file: {e}")
