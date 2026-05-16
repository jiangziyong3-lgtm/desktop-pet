from PySide6.QtGui import QGuiApplication

from states.base_state import BaseState
from config import ENERGY_WAKE


class SleepState(BaseState):
    """睡觉状态：移到屏幕底部，暂停属性衰减，精力恢复"""

    def on_enter(self):
        self.ctx.animator.play("sleep")
        self.ctx.attributes.sleeping = True
        screen = QGuiApplication.primaryScreen().availableGeometry()
        x = self.ctx.x()
        y = screen.bottom() - self.ctx.height() - 10
        self.ctx.move(x, y)
        self._wake_checked = False

    def on_exit(self):
        self.ctx.attributes.sleeping = False
        self._wake_checked = False

    def check_auto_transition(self):
        if not self._wake_checked:
            self._wake_checked = True
            return None
        if self.ctx.attributes.energy >= ENERGY_WAKE:
            return "idle"
        return None
