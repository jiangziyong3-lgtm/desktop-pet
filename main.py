import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QFont

from pet_window import PetWindow
from tray import TrayManager
from i18n import set_language
from save_manager import SAVE_FILE


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Desktop Pet")
    app.setQuitOnLastWindowClosed(False)

    font = QFont("Microsoft YaHei", 9)
    app.setFont(font)

    # 加载语言设置
    _load_language()

    pet = PetWindow()

    # 尝试加载存档
    loaded = pet.save_manager.load()
    if not loaded:
        pet.show()
    else:
        pet.show()
        # 加载后如果精力低于临界值，自动进入睡觉
        if pet.attributes.energy <= 10:
            pet.state_machine.transition_to("sleep")

    tray = TrayManager(pet, app)
    pet._tray = tray

    sys.exit(app.exec())


def _load_language():
    import json
    try:
        with open(SAVE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        lang = data.get("language", "zh")
        set_language(lang)
    except Exception:
        set_language("zh")


if __name__ == "__main__":
    main()
