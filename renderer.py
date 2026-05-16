from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter
from PySide6.QtCore import Qt

from config import PIXEL_SIZE, PALETTE


class Renderer(QWidget):
    """逐像素绘制精灵的渲染器"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.sprite = None
        self.facing_right = True
        self.setAttribute(Qt.WA_TransparentForMouseEvents)

    def set_sprite(self, sprite):
        self.sprite = sprite
        self.update()

    def paintEvent(self, event):
        if not self.sprite:
            return
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing, False)
        rows = len(self.sprite)
        cols = len(self.sprite[0]) if rows > 0 else 0
        for y in range(rows):
            for x in range(cols):
                idx = self.sprite[y][x]
                color = PALETTE.get(idx)
                if color:
                    draw_x = x if self.facing_right else (cols - 1 - x)
                    p.fillRect(
                        draw_x * PIXEL_SIZE,
                        y * PIXEL_SIZE,
                        PIXEL_SIZE,
                        PIXEL_SIZE,
                        color,
                    )
        p.end()
