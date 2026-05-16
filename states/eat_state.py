from states.base_state import BaseState


class EatState(BaseState):
    """吃东西状态：播放动画，结束后回到 idle"""

    def on_enter(self):
        self.ctx.animator.play("eat")

    def check_auto_transition(self):
        return None  # 由 Animator.animation_finished 触发转换
