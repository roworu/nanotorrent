import os
import shutil
import logging


class FileManager:
    @staticmethod
    def move_completed_torrent(status):
        """Move completed torrent files to the target folder."""
        incomplete_folder = os.path.join(status.save_path, ".incomplete")
        target_folder = os.path.dirname(status.save_path)

        try:
            for file in status.files:
                src = os.path.join(incomplete_folder, file.path)
                dst = os.path.join(target_folder, file.path)
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                shutil.move(src, dst)

            logging.info(f"Moved completed torrent: {status.name}")
        except Exception as e:
            logging.error(f"Failed to move completed torrent: {status.name}. Error: {e}")
