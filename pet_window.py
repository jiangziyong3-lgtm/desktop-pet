from PySide6.QtWidgets import (
    QWidget, QMenu, QApplication, QDialog, QVBoxLayout,
    QHBoxLayout, QLabel, QProgressBar, QFrame, QPushButton,
)
from PySide6.QtGui import (
    QPainter, QBitmap, QGuiApplication, QAction,
    QCursor, QMouseEvent,
)
from PySide6.QtCore import Qt, Signal, QPoint, QTimer

from config import PIXEL_SIZE, PALETTE
from renderer import Renderer
from animator import Animator
from state_machine import StateMachine
from attributes import Attributes
from save_manager import SaveManager


DRAG_THRESHOLD = 5


class PetWindow(QWidget):
    """桌面宠物主窗口 — 透明、无边框、置顶、可拖拽"""

    feed_requested = Signal()
    sleep_requested = Signal()

    def __init__(self):
        super().__init__()
        self._setup_window()
        self._setup_subsystems()
        self._setup_drag()
        self._connect_signals()
        self._position_initial()
        self._setup_autosave()

    def _setup_window(self):
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.WindowStaysOnTopHint
            | Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

    def _setup_subsystems(self):
        # 渲染器
        self.renderer = Renderer(self)

        # 动画器
        self.animator = Animator(self)

        # 属性系统
        self.attributes = Attributes(self)

        # 状态机（依赖 animator 和 attributes，后创建）
        self.state_machine = StateMachine(self)

        # 存档管理
        self.save_manager = SaveManager(self)

        # 初始渲染
        from sprites import IDLE_0
        sprite_w = len(IDLE_0[0]) * PIXEL_SIZE
        sprite_h = len(IDLE_0) * PIXEL_SIZE
        self.renderer.setFixedSize(sprite_w, sprite_h)
        self.setFixedSize(sprite_w, sprite_h)
        self.renderer.set_sprite(IDLE_0)
        self.update_mask()

    def _setup_drag(self):
        self._drag_origin: QPoint | None = None
        self._window_origin: QPoint | None = None
        self._press_pos: QPoint | None = None
        self._is_dragging = False

    def _setup_autosave(self):
        self._autosave_timer = QTimer(self)
        self._autosave_timer.timeout.connect(self.save_manager.auto_save)
        self._autosave_timer.start(300000)  # 每 5 分钟

    def _connect_signals(self):
        # 动画帧变化 → 渲染器
        self.animator.frame_changed.connect(self._on_frame_changed)

        # 非循环动画结束 → 状态转换
        self.animator.animation_finished.connect(self._on_animation_finished)

        # 状态变化（用于日志/调试，暂不处理）
        # self.state_machine.state_changed.connect(...)

        # 属性临界 → 强制睡觉
        self.attributes.hunger_critical.connect(lambda: self.state_machine.transition_to("sleep"))
        self.attributes.energy_critical.connect(lambda: self.state_machine.transition_to("sleep"))

        # 右键菜单 → 动作
        self.feed_requested.connect(self._open_shop)
        self.sleep_requested.connect(lambda: self.state_machine.transition_to("sleep"))

    def _on_frame_changed(self, sprite):
        self.renderer.set_sprite(sprite)
        self.update_mask()

    def _on_animation_finished(self, anim_name: str):
        if anim_name == "eat":
            self.state_machine.transition_to("idle")
        elif anim_name == "happy":
            self.state_machine.transition_to("idle")

    # ── 遮罩（透明区域穿透） ──

    def update_mask(self):
        sprite = self.renderer.sprite
        if not sprite:
            return
        scale = PIXEL_SIZE
        rows = len(sprite)
        cols = len(sprite[0]) if rows > 0 else 0
        w = cols * scale
        h = rows * scale
        bitmap = QBitmap(w, h)
        bitmap.clear()
        p = QPainter(bitmap)
        for y in range(rows):
            for x in range(cols):
                if PALETTE.get(sprite[y][x]):
                    p.fillRect(x * scale, y * scale, scale, scale, Qt.GlobalColor.white)
        p.end()
        self.setMask(bitmap)

    # ── 初始位置 ──

    def _position_initial(self):
        screen = QGuiApplication.primaryScreen().availableGeometry()
        x = screen.right() - self.width() - 100
        y = screen.bottom() - self.height() - 100
        self.move(x, y)

    # ── 鼠标事件 ──

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self._drag_origin = event.globalPosition().toPoint()
            self._window_origin = self.pos()
            self._press_pos = event.globalPosition().toPoint()
            self._is_dragging = False
        elif event.button() == Qt.MouseButton.MiddleButton:
            self._show_status()

    def mouseMoveEvent(self, event: QMouseEvent):
        if self._drag_origin is not None:
            delta = event.globalPosition().toPoint() - self._drag_origin
            if not self._is_dragging and delta.manhattanLength() >= DRAG_THRESHOLD:
                self._is_dragging = True
                self.state_machine.transition_to("drag")
            if self._is_dragging:
                self.move(self._window_origin + delta)

    def mouseReleaseEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            was_dragging = self._is_dragging
            self._drag_origin = None
            self._window_origin = None
            self._press_pos = None
            self._is_dragging = False
            if was_dragging:
                self.state_machine.transition_to("idle")
            else:
                # 单击 → 立即开心
                self.attributes.happiness = min(100, self.attributes.happiness + 5)
                self.attributes.happiness_changed.emit(self.attributes.happiness)
                self.state_machine.transition_to("happy")

    def mouseDoubleClickEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self.attributes.happiness = min(100, self.attributes.happiness + 10)
            self.attributes.happiness_changed.emit(self.attributes.happiness)
            self.state_machine.transition_to("happy")

    # ── 右键菜单 ──

    def contextMenuEvent(self, event):
        menu = QMenu(self)
        menu.setStyleSheet("""
            QMenu {
                background: #2d2d2d;
                color: #f0f0e0;
                border: 1px solid #555;
                padding: 4px;
            }
            QMenu::item {
                padding: 6px 24px;
            }
            QMenu::item:selected {
                background: #ff8800;
                color: #1a1a1a;
            }
        """)

        feed_action = QAction("喂食", self)
        feed_action.triggered.connect(self.feed_requested.emit)
        menu.addAction(feed_action)

        sleep_action = QAction("睡觉", self)
        sleep_action.triggered.connect(self.sleep_requested.emit)
        menu.addAction(sleep_action)

        if self.state_machine.current == "sleep":
            wake_action = QAction("唤醒", self)
            wake_action.triggered.connect(lambda: self.state_machine.transition_to("idle"))
            menu.addAction(wake_action)

        menu.addSeparator()

        quit_action = QAction("退出", self)
        quit_action.triggered.connect(self._quit)
        menu.addAction(quit_action)

        menu.exec(QCursor.pos())

    # ── 商店 ──

    def _open_shop(self):
        from shop.shop_window import ShopWindow
        shop = ShopWindow(self.attributes)
        shop.feed_requested.connect(self._on_feed)
        shop.show()

    def _on_feed(self, item: dict):
        self.attributes.apply_item_effects(item)
        self.state_machine.transition_to("eat")

    # ── 状态面板（鼠标中键） ──

    def _show_status(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("状态")
        dialog.setFixedSize(240, 200)
        dialog.setWindowFlags(
            Qt.WindowType.Dialog
            | Qt.WindowType.WindowStaysOnTopHint
        )
        dialog.setStyleSheet("""
            QDialog { background: #1a1a1a; color: #f0f0e0; }
            QLabel { color: #f0f0e0; }
            QProgressBar {
                border: 1px solid #444;
                border-radius: 3px;
                background: #2d2d2d;
                height: 12px;
                text-align: center;
                font-size: 9px;
            }
            QProgressBar::chunk {
                border-radius: 2px;
            }
        """)

        layout = QVBoxLayout(dialog)
        layout.setSpacing(6)

        layout.addWidget(QLabel(f"💰 金币: {int(self.attributes.coins)}"))

        for label, value, color in [
            ("饱食度", self.attributes.hunger, "#ff8800"),
            ("开心值", self.attributes.happiness, "#ff4488"),
            ("精力值", self.attributes.energy, "#4488ff"),
        ]:
            row = QHBoxLayout()
            name_label = QLabel(label)
            name_label.setFixedWidth(45)
            row.addWidget(name_label)
            bar = QProgressBar()
            bar.setRange(0, 100)
            bar.setValue(int(value))
            bar.setFormat(f"{int(value)}")
            bar.setStyleSheet(f"QProgressBar::chunk {{ background: {color}; }}")
            row.addWidget(bar)
            layout.addLayout(row)

        close_btn = QPushButton("关闭")
        close_btn.clicked.connect(dialog.close)
        close_btn.setStyleSheet("""
            QPushButton {
                background: #444; color: #f0f0e0;
                border: 1px solid #555; border-radius: 4px;
                padding: 4px 12px;
            }
            QPushButton:hover { background: #ff8800; color: #1a1a1a; }
        """)
        layout.addWidget(close_btn, alignment=Qt.AlignmentFlag.AlignCenter)

        dialog.exec()

    # ── 退出 ──

    def _quit(self):
        self.save_manager.save()
        self.state_machine.timer.stop()
        self.attributes.timer.stop()
        QApplication.instance().quit()
