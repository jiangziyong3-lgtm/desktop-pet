from PySide6.QtWidgets import QSystemTrayIcon, QMenu, QApplication
from PySide6.QtGui import QIcon, QPixmap, QPainter, QColor, QAction
from PySide6.QtCore import Qt

from i18n import _


def _build_tray_icon() -> QIcon:
    """手绘像素小机器人托盘图标"""
    pixmap = QPixmap(16, 16)
    pixmap.fill(Qt.GlobalColor.transparent)
    p = QPainter(pixmap)
    # 简化版小机器人
    colors = {
        "body": QColor("#2d2d2d"),
        "screen": QColor("#ff8800"),
        "antenna": QColor("#ff4444"),
        "led": QColor("#4488ff"),
    }
    pixels = [
        (7,0,colors["antenna"]), (7,1,colors["antenna"]),
        (5,2,colors["body"]), (6,2,colors["body"]), (7,2,colors["body"]), (8,2,colors["body"]),
        (4,3,colors["body"]), (5,3,colors["body"]), (8,3,colors["body"]), (9,3,colors["body"]),
        (4,4,colors["body"]), (5,4,colors["screen"]), (6,4,colors["screen"]), (7,4,colors["screen"]), (8,4,colors["screen"]), (9,4,colors["body"]),
        (4,5,colors["body"]), (5,5,colors["screen"]), (6,5,colors["led"]), (7,5,colors["led"]), (8,5,colors["screen"]), (9,5,colors["body"]),
        (4,6,colors["body"]), (5,6,colors["screen"]), (6,6,colors["screen"]), (7,6,colors["screen"]), (8,6,colors["screen"]), (9,6,colors["body"]),
        (4,7,colors["body"]), (5,7,colors["body"]), (6,7,colors["body"]), (7,7,colors["body"]), (8,7,colors["body"]), (9,7,colors["body"]),
        (5,8,colors["body"]), (6,8,colors["body"]), (7,8,colors["body"]), (8,8,colors["body"]),
        (5,9,colors["body"]), (6,9,colors["body"]), (7,9,colors["body"]), (8,9,colors["body"]),
        (5,10,colors["body"]), (7,10,colors["body"]),
        (5,11,colors["body"]), (7,11,colors["body"]),
        (4,12,colors["led"]), (7,12,colors["led"]),
    ]
    for x, y, color in pixels:
        p.fillRect(x, y, 1, 1, color)
    p.end()
    return QIcon(pixmap)


class TrayManager:
    """系统托盘管理器"""

    def __init__(self, pet_window, app: QApplication):
        self.pet = pet_window
        self.app = app

        self.icon = _build_tray_icon()
        self.tray = QSystemTrayIcon(self.icon, app)
        self.tray.setToolTip(_("app_name"))

        self._build_menu()
        self.tray.show()

    def _build_menu(self):
        menu = QMenu()

        show_action = QAction(_("show_pet"), menu)
        show_action.triggered.connect(self.pet.show)
        menu.addAction(show_action)

        hide_action = QAction(_("hide_pet"), menu)
        hide_action.triggered.connect(self.pet.hide)
        menu.addAction(hide_action)

        menu.addSeparator()

        feed_action = QAction(_("feed"), menu)
        feed_action.triggered.connect(self.pet.feed_requested.emit)
        menu.addAction(feed_action)

        sleep_action = QAction(_("sleep"), menu)
        sleep_action.triggered.connect(self.pet.sleep_requested.emit)
        menu.addAction(sleep_action)

        menu.addSeparator()

        quit_action = QAction(_("quit"), menu)
        quit_action.triggered.connect(self._quit)
        menu.addAction(quit_action)

        self.tray.setContextMenu(menu)

    def _quit(self):
        self.pet.save_manager.save()
        self.tray.hide()
        self.app.quit()

    def rebuild_menu(self):
        self.tray.setToolTip(_("app_name"))
        self._build_menu()
