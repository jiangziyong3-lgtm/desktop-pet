import random
from PySide6.QtCore import QTimer

from states.base_state import BaseState
from config import WALK_COOLDOWN_MIN, WALK_COOLDOWN_MAX, HUNGER_CRITICAL, ENERGY_CRITICAL, ENERGY_WALK_MIN, HUNGER_WALK_MIN


class IdleState(BaseState):
    """待机状态：随机触发走路，检测饥饿/疲劳阈值"""

    def on_enter(self):
        happiness = self.ctx.attributes.happiness
        if happiness < 30:
            anim = "idle_sad"
        elif happiness > 70:
            anim = "idle_happy"
        else:
            anim = "idle"
        self.ctx.animator.play(anim)
        self._schedule_walk()

    def on_exit(self):
        if hasattr(self, "_walk_timer") and self._walk_timer:
            self._walk_timer.stop()

    def _schedule_walk(self):
        delay = random.randint(WALK_COOLDOWN_MIN, WALK_COOLDOWN_MAX)
        self._walk_timer = QTimer(self.ctx)
        self._walk_timer.setSingleShot(True)
        self._walk_timer.timeout.connect(self._try_walk)
        self._walk_timer.start(delay)

    def _try_walk(self):
        if self.ctx.state_machine.current != "idle":
            return
        attrs = self.ctx.attributes
        if attrs.energy >= ENERGY_WALK_MIN and attrs.hunger >= HUNGER_WALK_MIN:
            self.ctx.state_machine.transition_to("walk")

    def check_auto_transition(self):
        attrs = self.ctx.attributes
        if attrs.energy <= ENERGY_CRITICAL:
            return "sleep"
        if attrs.hunger <= HUNGER_CRITICAL:
            return "sleep"
        return None
