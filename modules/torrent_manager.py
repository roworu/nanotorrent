import libtorrent as lt
import time
import logging
from threading import Thread


class TorrentManager:
    def __init__(self):
        self.session = lt.session()
        self.session.listen_on(6881, 6891)
        self.torrents = []
        self.running = True

        # Start a background thread to manage the session
        self.thread = Thread(target=self._manage_session, daemon=True)
        self.thread.start()

    def add_torrent(self, file_path, save_path):
        """Add a torrent to the session."""
        try:
            info = lt.torrent_info(file_path)
            params = {
                "save_path": save_path,
                "storage_mode": lt.storage_mode_t.storage_mode_sparse,
                "ti": info,
            }
            handle = self.session.add_torrent(params)
            self.torrents.append(handle)
            logging.info(f"Added torrent: {info.name()}")
        except Exception as e:
            logging.error(f"Failed to add torrent: {file_path}. Error: {e}")
            raise

    def get_torrents(self):
        """Get the latest list of torrents and their statuses."""
        statuses = []
        for torrent in self.torrents:
            status = torrent.status()  # Fetch the latest status
            statuses.append({
                "name": status.name,
                "progress": status.progress,
                "download_rate": status.download_rate,
                "upload_rate": status.upload_rate,
                "peers": status.num_peers,
                "state": self._get_state(status.state),
            })
        return statuses

    def _manage_session(self):
        """Background thread to manage the libtorrent session."""
        while self.running:
            self.session.post_torrent_updates()  # Post updates to refresh statuses
            time.sleep(1)

    def stop(self):
        """Stop the torrent manager and its background thread."""
        self.running = False
        self.session.pause()
        logging.info("Torrent manager stopped.")

    @staticmethod
    def _get_state(state_code):
        """Map torrent state codes to user-friendly strings."""
        states = {
            lt.torrent_status.queued_for_checking: "Queued",
            lt.torrent_status.checking_files: "Checking",
            lt.torrent_status.downloading_metadata: "Downloading Metadata",
            lt.torrent_status.downloading: "Downloading",
            lt.torrent_status.finished: "Finished",
            lt.torrent_status.seeding: "Seeding",
            lt.torrent_status.allocating: "Allocating",
            lt.torrent_status.error: "Error",
        }
        return states.get(state_code, "Unknown")
