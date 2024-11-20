from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView
from PyQt6.QtGui import QColor


def setup_table(parent):
    """Create and configure the torrent table."""
    table = QTableWidget(parent)
    table.setColumnCount(4)
    table.setHorizontalHeaderLabels(["Name", "Progress", "Download", "Upload"])

    # Fix resize mode
    header = table.horizontalHeader()
    header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
    header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
    header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
    header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)

    return table


def update_table(table, torrents):
    """Update the table with the latest torrent statuses."""
    table.setRowCount(len(torrents))
    for i, torrent in enumerate(torrents):
        name_item = QTableWidgetItem(torrent["name"])
        progress_item = QTableWidgetItem(f"{torrent['progress'] * 100:.2f}%")
        download_item = QTableWidgetItem(f"{torrent['download_rate'] / 1000:.2f} kB/s")
        upload_item = QTableWidgetItem(f"{torrent['upload_rate'] / 1000:.2f} kB/s")

        # Set items as non-editable
        for item in (name_item, progress_item, download_item, upload_item):
            item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)

        table.setItem(i, 0, name_item)
        table.setItem(i, 1, progress_item)
        table.setItem(i, 2, download_item)
        table.setItem(i, 3, upload_item)

        if torrent["progress"] >= 1.0:
            set_row_color(table, i, QColor(0, 255, 0, 20))
        else:
            set_row_color(table, i, QColor(0, 0, 255, 20))


def set_row_color(table, row, color):
    """Set the background color for a specific row."""
    for col in range(table.columnCount()):
        item = table.item(row, col)
        if item:
            item.setBackground(color)
