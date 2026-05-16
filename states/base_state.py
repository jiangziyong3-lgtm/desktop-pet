from typing import Optional


class BaseState:
    """状态基类"""

    def __init__(self, context: "PetWindow"):
        self.ctx = context

    def on_enter(self):
        pass

    def on_exit(self):
        pass

    def on_tick(self):
        pass

    def check_auto_transition(self) -> Optional[str]:
        """返回要自动转换的目标状态名，不需要转换则返回 None"""
        return None
