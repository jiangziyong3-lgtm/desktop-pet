from PySide6.QtCore import QObject, QTimer, Signal

from sprites import ANIMATIONS


class Animator(QObject):
    """动画播放器：管理帧切换和播放状态"""

    frame_changed = Signal(object)  # 发送当前帧精灵数据
    animation_finished = Signal(str)  # 非循环动画播放完毕，发送动画名

    def __init__(self, parent=None):
        super().__init__(parent)
        self._current_anim = "idle"
        self._frame_index = 0
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._next_frame)

    @property
    def current_animation(self):
        return self._current_anim

    @property
    def current_sprite(self):
        return ANIMATIONS[self._current_anim]["frames"][self._frame_index]

    def play(self, name: str):
        if name not in ANIMATIONS:
            return
        info = ANIMATIONS[name]
        self._current_anim = name
        self._frame_index = 0
        interval = int(1000 / info["fps"])
        self._timer.start(interval)
        self.frame_changed.emit(self.current_sprite)

    def _next_frame(self):
        info = ANIMATIONS[self._current_anim]
        frames = info["frames"]
        self._frame_index += 1
        if self._frame_index >= len(frames):
            if info["loop"]:
                self._frame_index = 0
            else:
                self._timer.stop()
                self.animation_finished.emit(self._current_anim)
                return
        self.frame_changed.emit(self.current_sprite)

    def stop(self):
        self._timer.stop()

    def resume(self):
        info = ANIMATIONS[self._current_anim]
        interval = int(1000 / info["fps"])
        self._timer.start(interval)
