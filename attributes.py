from PySide6.QtCore import QObject, QTimer, Signal

from config import (
    HUNGER_DECAY, HAPPINESS_DECAY, ENERGY_DECAY, ENERGY_RECOVER,
    COIN_GAIN, TICK_INTERVAL,
)


class Attributes(QObject):
    """宠物属性系统 — 饱食度 / 开心值 / 精力值 / 金币"""

    hunger_changed = Signal(float)
    happiness_changed = Signal(float)
    energy_changed = Signal(float)
    coins_changed = Signal(int)
    hunger_critical = Signal()
    energy_critical = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.hunger = 100.0
        self.happiness = 80.0
        self.energy = 100.0
        self.coins = 50
        self.sleeping = False

        self.timer = QTimer(self)
        self.timer.timeout.connect(self._decay)
        self.timer.start(TICK_INTERVAL)

        self._coin_accum = 0.0

    def _decay(self):
        dt = TICK_INTERVAL / 1000.0  # 秒

        # 饱食度持续衰减
        old_hunger = self.hunger
        self.hunger = max(0, self.hunger - HUNGER_DECAY * dt)
        if int(old_hunger) != int(self.hunger):
            self.hunger_changed.emit(self.hunger)
        if old_hunger > 10 and self.hunger <= 10:
            self.hunger_critical.emit()

        # 开心值持续衰减
        old_happiness = self.happiness
        self.happiness = max(0, self.happiness - HAPPINESS_DECAY * dt)
        if int(old_happiness) != int(self.happiness):
            self.happiness_changed.emit(self.happiness)

        # 精力值
        old_energy = self.energy
        if self.sleeping:
            self.energy = min(100, self.energy + ENERGY_RECOVER * dt)
        else:
            self.energy = max(0, self.energy - ENERGY_DECAY * dt)
        if int(old_energy) != int(self.energy):
            self.energy_changed.emit(self.energy)
        if old_energy > 10 and self.energy <= 10:
            self.energy_critical.emit()

        # 金币被动收入
        self._coin_accum += COIN_GAIN * dt
        earned = int(self._coin_accum)
        if earned > 0:
            self._coin_accum -= earned
            self.coins += earned
            self.coins_changed.emit(self.coins)

    def apply_item_effects(self, item: dict):
        self.hunger = min(100, self.hunger + item.get("hunger", 0))
        self.happiness = min(100, self.happiness + item.get("happiness", 0))
        self.energy = min(100, self.energy + item.get("energy", 0))
        self.hunger_changed.emit(self.hunger)
        self.happiness_changed.emit(self.happiness)
        self.energy_changed.emit(self.energy)
