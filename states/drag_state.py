from states.base_state import BaseState


class DragState(BaseState):
    """拖拽状态：暂停动画，跟随鼠标"""

    def on_enter(self):
        self.ctx.animator.stop()

    def on_exit(self):
        pass

    def check_auto_transition(self):
        return None
