import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QFont

from pet_window import PetWindow
from tray import TrayManager


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Desktop Pet")
    app.setQuitOnLastWindowClosed(False)

    font = QFont("Microsoft YaHei", 9)
    app.setFont(font)

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

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
