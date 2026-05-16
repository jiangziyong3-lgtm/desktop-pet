from PySide6.QtCore import QObject, QTimer, Signal

from states import IdleState, WalkState, SleepState, EatState, HappyState, DragState


class StateMachine(QObject):
    """有限状态机：管理状态转换和自动 tick"""

    state_changed = Signal(str, str)  # (old_state, new_state)

    TRANSITIONS = {
        "idle":  ["walk", "sleep", "happy", "eat", "drag"],
        "walk":  ["idle", "drag"],
        "sleep": ["idle", "drag"],
        "eat":   ["idle"],
        "happy": ["idle"],
        "drag":  ["idle"],
    }

    def __init__(self, pet_window: "PetWindow"):
        super().__init__(pet_window)
        self.ctx = pet_window
        self.current = "idle"
        self.states = {
            "idle":  IdleState(pet_window),
            "walk":  WalkState(pet_window),
            "sleep": SleepState(pet_window),
            "eat":   EatState(pet_window),
            "happy": HappyState(pet_window),
            "drag":  DragState(pet_window),
        }

        self.timer = QTimer(self)
        self.timer.timeout.connect(self._tick)
        self.timer.start(200)  # 每 200ms tick 一次

    def transition_to(self, new_state: str) -> bool:
        if new_state not in self.TRANSITIONS.get(self.current, []):
            return False
        old = self.current
        self.states[old].on_exit()
        self.current = new_state
        self.states[new_state].on_enter()
        self.state_changed.emit(old, new_state)
        return True

    def _tick(self):
        self.states[self.current].on_tick()
        transition = self.states[self.current].check_auto_transition()
        if transition:
            self.transition_to(transition)
