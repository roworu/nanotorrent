import libtorrent as lt
import logging


class SessionManager:
    def __init__(self, settings):
        self.session = lt.session()
        self.session.listen_on(6881, 6891)
        self.settings = settings
        self._apply_speed_limits()

    def _apply_speed_limits(self):
        """Apply download and upload speed limits from settings."""
        try:
            max_download_speed = int(self.settings.get("Speed", "max_download_speed"))
            max_upload_speed = int(self.settings.get("Speed", "max_upload_speed"))

            self.session.set_download_rate_limit(max_download_speed)
            self.session.set_upload_rate_limit(max_upload_speed)

            logging.info(f"Speed limits applied: download={max_download_speed} bytes/s, upload={max_upload_speed} bytes/s")
        except ValueError as e:
            logging.warning(f"Invalid speed limit values: {e}")
            self.session.set_download_rate_limit(0)
            self.session.set_upload_rate_limit(0)

    def pause(self):
        """Pause the session."""
        self.session.pause()

    def get_session(self):
        """Return the libtorrent session."""
        return self.session
