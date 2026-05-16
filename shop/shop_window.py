from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QFrame, QScrollArea, QWidget, QGridLayout,
)
from PySide6.QtCore import Qt, Signal

from shop.shop_data import ITEMS
from i18n import _


class ShopWindow(QDialog):
    """商店窗口"""

    feed_requested = Signal(dict)  # 发出要喂食的商品

    def __init__(self, attributes, parent=None):
        super().__init__(parent)
        self.attributes = attributes
        self._setup_ui()
        self._setup_style()
        self.attributes.coins_changed.connect(self._update_coins)

    def _setup_ui(self):
        self.setWindowTitle(_("shop"))
        self.setFixedSize(460, 480)
        self.setWindowFlags(
            Qt.WindowType.Dialog
            | Qt.WindowType.WindowStaysOnTopHint
        )

        layout = QVBoxLayout(self)
        layout.setSpacing(8)

        # 金币余额
        coins_layout = QHBoxLayout()
        self.coins_label = QLabel()
        coins_layout.addStretch()
        coins_layout.addWidget(self.coins_label)
        layout.addLayout(coins_layout)
        self._update_coins(self.attributes.coins)

        # 商品网格
        grid = QGridLayout()
        grid.setSpacing(8)

        for i, item in enumerate(ITEMS):
            card = self._build_card(item)
            row, col = divmod(i, 2)
            grid.addWidget(card, row, col)

        layout.addLayout(grid)

        # 关闭按钮
        close_btn = QPushButton(_("close"))
        close_btn.clicked.connect(self.close)
        layout.addWidget(close_btn, alignment=Qt.AlignmentFlag.AlignCenter)

    def _build_card(self, item: dict) -> QFrame:
        card = QFrame()
        card.setObjectName("card")
        card.setFixedSize(215, 160)

        card_layout = QVBoxLayout(card)
        card_layout.setSpacing(4)

        # 图标和名称
        header = QHBoxLayout()
        icon_label = QLabel(item["icon"])
        icon_label.setStyleSheet("font-size: 20px;")
        item_name = _(f"item_{item['id']}_name")
        name_label = QLabel(item_name)
        name_label.setStyleSheet("font-weight: bold; font-size: 12px;")
        header.addWidget(icon_label)
        header.addWidget(name_label)
        header.addStretch()
        card_layout.addLayout(header)

        # 描述
        item_desc = _(f"item_{item['id']}_desc")
        desc_label = QLabel(item_desc)
        desc_label.setWordWrap(True)
        desc_label.setStyleSheet("color: #888; font-size: 10px;")
        card_layout.addWidget(desc_label)

        # 效果
        effects = []
        if item["hunger"]:
            effects.append(f"{_('hunger')}+{item['hunger']}")
        if item["happiness"]:
            effects.append(f"{_('happiness')}+{item['happiness']}")
        if item["energy"]:
            v = item["energy"]
            effects.append(f"{_('energy')}{'+' if v > 0 else ''}{v}")

        effect_label = QLabel(" | ".join(effects))
        effect_label.setStyleSheet("color: #aaa; font-size: 10px;")
        card_layout.addWidget(effect_label)

        # 价格和按钮
        bottom = QHBoxLayout()
        price_label = QLabel(f"💰 {item['price']}")
        price_label.setStyleSheet("color: #ffaa00; font-size: 12px;")
        bottom.addWidget(price_label)
        bottom.addStretch()

        buy_btn = QPushButton(_("buy_and_feed"))
        buy_btn.setFixedSize(100, 28)
        buy_btn.clicked.connect(lambda: self._buy_and_feed(item))
        bottom.addWidget(buy_btn)
        card_layout.addLayout(bottom)

        return card

    def _buy_and_feed(self, item: dict):
        if self.attributes.coins >= item["price"]:
            self.attributes.coins -= item["price"]
            self.attributes.coins_changed.emit(self.attributes.coins)
            self.feed_requested.emit(item)
            self.close()

    def _update_coins(self, coins: int):
        self.coins_label.setText(f"💰 {_('coins')}: {coins}")

    def _setup_style(self):
        self.setStyleSheet("""
            QDialog {
                background: #1a1a1a;
                color: #f0f0e0;
            }
            QLabel {
                color: #f0f0e0;
            }
            QFrame#card {
                background: #2d2d2d;
                border: 1px solid #444;
                border-radius: 8px;
                padding: 8px;
            }
            QPushButton {
                background: #444;
                color: #f0f0e0;
                border: 1px solid #555;
                border-radius: 4px;
                padding: 4px 12px;
            }
            QPushButton:hover {
                background: #ff8800;
                color: #1a1a1a;
                border-color: #ff8800;
            }
        """)
