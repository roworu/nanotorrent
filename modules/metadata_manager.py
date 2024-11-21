import os
import json
import libtorrent as lt
import logging

# FIXME metadata unable to load on app startup, no idea why
class MetadataManager:
    
    def __init__(self, metadata_file="torrent_metadata.json"):
        self.metadata_file = metadata_file

    def save_metadata(self, torrents):
        """Save metadata for active torrents."""
        try:
            data = {"torrents": []}
            for torrent in torrents:
                status = torrent.status()
                torrent_info = torrent.get_torrent_info()
                save_path = status.save_path.rstrip(".incomplete")
                torrent_file_path = os.path.join(save_path, f"{status.name}.torrent")

                # Save .torrent file
                with open(torrent_file_path, "wb") as f:
                    f.write(torrent_info.metadata())

                data["torrents"].append({
                    "torrent_file": torrent_file_path,
                    "save_path": save_path,
                    "progress": status.progress,
                    "name": status.name,
                })

            # Write metadata to file
            with open(self.metadata_file, "w") as f:
                json.dump(data, f, indent=4)

            logging.info("Metadata successfully saved")
        except Exception as e:
            logging.error(f"Failed to save metadata: {e}")

    def load_metadata(self):
        """Load metadata from file."""
        if not os.path.exists(self.metadata_file):
            logging.info("No metadata file found, starting fresh")
            return []

        try:
            with open(self.metadata_file, "r") as f:
                return json.load(f).get("torrents", [])
        except Exception as e:
            logging.error(f"Failed to load metadata: {e}")
            return []
