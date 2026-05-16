from states.base_state import BaseState


class HappyState(BaseState):
    """开心状态：短暂播放开心动画，结束后回到 idle"""

    def on_enter(self):
        self.ctx.animator.play("happy")

    def check_auto_transition(self):
        return None  # 由 Animator.animation_finished 触发转换
