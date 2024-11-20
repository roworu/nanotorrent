from PyQt6.QtWidgets import QMenu, QMenuBar, QMessageBox


def setup_menu(parent):
    """Create and configure the menu bar."""
    menu_bar = QMenuBar(parent)

    # File Menu
    file_menu = QMenu("File", parent)
    file_menu.addAction("Add Torrent", parent.add_torrent)
    file_menu.addAction("Settings", parent.open_settings)
    file_menu.addAction("Exit", parent.close)
    menu_bar.addMenu(file_menu)

    # Help Menu
    help_menu = QMenu("Help", parent)
    help_menu.addAction("About", lambda: QMessageBox.about(
        parent,
        "About",
        "NanoTorrent: A simple PyQt6-based torrent client."
    ))
    menu_bar.addMenu(help_menu)

    parent.setMenuBar(menu_bar)
