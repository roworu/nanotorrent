import logging
import libtorrent as lt
from .session_manager import SessionManager
from .metadata_manager import MetadataManager
from .file_manager import FileManager
import os


class TorrentManager:
    def __init__(self, settings):
        self.settings = settings
        self.session_manager = SessionManager(settings)
        self.metadata_manager = MetadataManager()
        self.file_manager = FileManager()
        self.torrents = []

        self._load_metadata()

    def _load_metadata(self):
        """Load torrents from metadata."""
        metadata = self.metadata_manager.load_metadata()
        for torrent_info in metadata:
            try:
                info = lt.torrent_info(torrent_info["torrent_file"])
                save_path = torrent_info["save_path"]
                params = {
                    "save_path": save_path,
                    "storage_mode": lt.storage_mode_t.storage_mode_sparse,
                    "ti": info,
                }
                handle = self.session_manager.get_session().add_torrent(params)
                self.torrents.append(handle)
            except Exception as e:
                logging.error(f"Failed to load torrent: {torrent_info}. Error: {e}")

    def add_torrent(self, torrent_file, save_path):
        """Add a new torrent."""
        try:
            incomplete_folder = os.path.join(save_path, ".incomplete")
            os.makedirs(incomplete_folder, exist_ok=True)

            info = lt.torrent_info(torrent_file)
            params = {
                "save_path": incomplete_folder,
                "storage_mode": lt.storage_mode_t.storage_mode_sparse,
                "ti": info,
            }
            handle = self.session_manager.get_session().add_torrent(params)
            self.torrents.append(handle)

            logging.info(f"Added torrent: {info.name()}")
        except Exception as e:
            logging.error(f"Failed to add torrent: {torrent_file}. Error: {e}")

    def get_torrents(self):
        """Get the list of torrents and their statuses."""
        statuses = []
        for torrent in self.torrents:
            try:
                status = torrent.status()
                statuses.append({
                    "name": status.name,
                    "progress": status.progress,
                    "download_rate": status.download_rate,
                    "upload_rate": status.upload_rate,
                    "peers": status.num_peers,
                    "state": self._get_state(status.state),
                })
            except Exception as e:
                logging.warning(f"Failed to retrieve status for a torrent. Error: {e}")
        return statuses

    def stop(self):
        """Stop the torrent manager."""
        self.metadata_manager.save_metadata(self.torrents)
        self.session_manager.pause()
        logging.info("Torrent manager stopped")



    @staticmethod
    def _get_state(state_code):
        """Map libtorrent state codes to user-friendly strings."""
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
