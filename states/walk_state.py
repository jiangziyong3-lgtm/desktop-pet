import random
from PySide6.QtGui import QGuiApplication

from states.base_state import BaseState
from config import WALK_SPEED, WALK_REACHED_THRESHOLD


class WalkState(BaseState):
    """走路状态：向随机目标移动"""

    def on_enter(self):
        self.ctx.animator.play("walk")
        screen = QGuiApplication.primaryScreen().availableGeometry()
        margin = 50
        self.target_x = random.randint(margin, screen.right() - margin - self.ctx.width())
        self.target_y = random.randint(margin, screen.bottom() - margin - self.ctx.height())

    def on_tick(self):
        dx = self.target_x - self.ctx.x()
        dy = self.target_y - self.ctx.y()
        dist = (dx ** 2 + dy ** 2) ** 0.5
        if dist < WALK_REACHED_THRESHOLD:
            self.ctx.state_machine.transition_to("idle")
            return

        ratio = WALK_SPEED / dist
        new_x = self.ctx.x() + int(dx * ratio)
        new_y = self.ctx.y() + int(dy * ratio)
        self.ctx.move(new_x, new_y)
        self.ctx.renderer.facing_right = (dx >= 0)

    def check_auto_transition(self):
        return None
