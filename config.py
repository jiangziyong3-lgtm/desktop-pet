from PySide6.QtGui import QColor

# 窗口
PIXEL_SIZE = 6  # 每个像素块的屏幕像素大小 (16x16 → 96x96)
TICK_INTERVAL = 200  # 状态机 tick 间隔 (ms)

# 属性衰减速率 (/秒)
HUNGER_DECAY = 0.5 / 60
HAPPINESS_DECAY = 0.3 / 60
ENERGY_DECAY = 0.4 / 60
ENERGY_RECOVER = 2.0 / 60
COIN_GAIN = 1.0 / 300

# 阈值
HUNGER_CRITICAL = 10
ENERGY_CRITICAL = 10
ENERGY_WAKE = 80
HUNGER_WALK_MIN = 10
ENERGY_WALK_MIN = 20

# 行走
WALK_SPEED = 3  # 像素/tick
WALK_REACHED_THRESHOLD = 5  # 到达目标距离阈值
WALK_COOLDOWN_MIN = 3000  # 走路冷却最小 ms
WALK_COOLDOWN_MAX = 10000  # 走路冷却最大 ms

# 调色板 (像素风机器人)
PALETTE = {
    0: None,                    # 透明
    1: QColor("#2d2d2d"),       # 轮廓线
    2: QColor("#ff8800"),       # 屏幕暖橙
    3: QColor("#f0f0e0"),       # 屏幕文字/高光
    4: QColor("#4488ff"),       # LED 蓝
    5: QColor("#555555"),       # 金属灰
    6: QColor("#ff4444"),       # 天线红
}
