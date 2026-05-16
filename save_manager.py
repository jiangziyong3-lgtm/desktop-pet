import json
import os
from datetime import datetime, timezone
from pathlib import Path

from config import HUNGER_DECAY, HAPPINESS_DECAY, ENERGY_DECAY, COIN_GAIN
from i18n import _current_lang


SAVE_FILE = Path(__file__).parent / "save.json"


class SaveManager:
    """存档管理：JSON 读写 + 离线时间补偿"""

    def __init__(self, pet_window):
        self.pet = pet_window

    def save(self):
        attrs = self.pet.attributes
        data = {
            "version": 1,
            "language": _current_lang,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "pet": {
                "x": self.pet.x(),
                "y": self.pet.y(),
                "facing_right": self.pet.renderer.facing_right,
            },
            "attributes": {
                "hunger": attrs.hunger,
                "happiness": attrs.happiness,
                "energy": attrs.energy,
                "coins": attrs.coins,
            },
        }
        with open(SAVE_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def load(self) -> bool:
        if not SAVE_FILE.exists():
            return False

        try:
            with open(SAVE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
        except (json.JSONDecodeError, KeyError):
            return False

        if data.get("version") != 1:
            return False

        # 恢复位置
        pet_data = data.get("pet", {})
        if "x" in pet_data and "y" in pet_data:
            self.pet.move(pet_data["x"], pet_data["y"])
        self.pet.renderer.facing_right = pet_data.get("facing_right", True)

        # 恢复属性 + 离线补偿
        attr_data = data.get("attributes", {})
        saved_time = datetime.fromisoformat(data["timestamp"])
        now = datetime.now(timezone.utc)
        delta_seconds = (now - saved_time).total_seconds()
        if delta_seconds < 0:
            delta_seconds = 0

        attrs = self.pet.attributes
        attrs.hunger = max(0, attr_data.get("hunger", 100) - HUNGER_DECAY * delta_seconds)
        attrs.happiness = max(0, attr_data.get("happiness", 80) - HAPPINESS_DECAY * delta_seconds)
        attrs.energy = max(0, attr_data.get("energy", 100) - ENERGY_DECAY * delta_seconds)
        attrs.coins = attr_data.get("coins", 50) + int(COIN_GAIN * delta_seconds)

        attrs.hunger_changed.emit(attrs.hunger)
        attrs.happiness_changed.emit(attrs.happiness)
        attrs.energy_changed.emit(attrs.energy)
        attrs.coins_changed.emit(attrs.coins)

        return True

    def auto_save(self):
        self.save()
