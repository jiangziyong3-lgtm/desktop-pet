from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QComboBox, QLineEdit, QFrame,
)
from PySide6.QtCore import Qt, Signal

from i18n import _, LANGUAGES, set_language, _current_lang
from config import GIFT_CODES


class SettingsWindow(QDialog):
    """设置窗口 - 语言切换 + 礼包码兑换"""

    language_changed = Signal(str)
    gift_redeemed = Signal(int)

    def __init__(self, attributes, parent=None):
        super().__init__(parent)
        self.attributes = attributes
        self._setup_ui()
        self._setup_style()

    def _setup_ui(self):
        self.setWindowTitle(_("settings"))
        self.setFixedSize(360, 280)
        self.setWindowFlags(
            Qt.WindowType.Dialog
            | Qt.WindowType.WindowStaysOnTopHint
        )

        layout = QVBoxLayout(self)
        layout.setSpacing(12)

        # 语言
        lang_label = QLabel(_("language"))
        lang_label.setStyleSheet("font-size: 12px; font-weight: bold;")
        layout.addWidget(lang_label)

        lang_row = QHBoxLayout()
        self.lang_combo = QComboBox()
        for code, name in LANGUAGES.items():
            self.lang_combo.addItem(name, code)
        idx = list(LANGUAGES.keys()).index(_current_lang)
        self.lang_combo.setCurrentIndex(idx)
        self.lang_combo.currentIndexChanged.connect(self._on_lang_changed)
        lang_row.addWidget(self.lang_combo)
        lang_row.addStretch()
        layout.addLayout(lang_row)

        # 分割线
        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        sep.setStyleSheet("background: #444;")
        layout.addWidget(sep)

        # 礼包码
        gift_label = QLabel(_("gift_code"))
        gift_label.setStyleSheet("font-size: 12px; font-weight: bold;")
        layout.addWidget(gift_label)

        gift_row = QHBoxLayout()
        self.gift_input = QLineEdit()
        self.gift_input.setPlaceholderText("IAMPOOR")
        gift_row.addWidget(self.gift_input)

        redeem_btn = QPushButton(_("redeem"))
        redeem_btn.setFixedWidth(80)
        redeem_btn.clicked.connect(self._on_redeem)
        gift_row.addWidget(redeem_btn)
        layout.addLayout(gift_row)

        self.gift_msg = QLabel("")
        self.gift_msg.setStyleSheet("color: #888; font-size: 10px;")
        self.gift_msg.setWordWrap(True)
        layout.addWidget(self.gift_msg)

        layout.addStretch()

        # 关闭
        close_btn = QPushButton(_("close"))
        close_btn.clicked.connect(self.close)
        layout.addWidget(close_btn, alignment=Qt.AlignmentFlag.AlignCenter)

    def _on_lang_changed(self, index: int):
        code = self.lang_combo.itemData(index)
        set_language(code)
        self._retranslate()
        self.language_changed.emit(code)

    def _retranslate(self):
        self.setWindowTitle(_("settings"))
        for i in range(self.layout().count()):
            w = self.layout().itemAt(i).widget()
            if w is None:
                continue

    def _on_redeem(self):
        code = self.gift_input.text().strip().upper()
        if code in GIFT_CODES:
            amount = GIFT_CODES[code]
            self.attributes.coins += amount
            self.attributes.coins_changed.emit(self.attributes.coins)
            self.gift_msg.setStyleSheet("color: #88ff88; font-size: 10px;")
            self.gift_msg.setText(_("gift_code_success", amount))
            self.gift_redeemed.emit(amount)
        else:
            self.gift_msg.setStyleSheet("color: #ff4444; font-size: 10px;")
            self.gift_msg.setText(_("gift_code_invalid"))

    def _setup_style(self):
        self.setStyleSheet("""
            QDialog {
                background: #1a1a1a;
                color: #f0f0e0;
            }
            QLabel {
                color: #f0f0e0;
            }
            QComboBox {
                background: #2d2d2d;
                color: #f0f0e0;
                border: 1px solid #555;
                border-radius: 4px;
                padding: 4px 8px;
                min-width: 140px;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox QAbstractItemView {
                background: #2d2d2d;
                color: #f0f0e0;
                selection-background-color: #ff8800;
                selection-color: #1a1a1a;
            }
            QLineEdit {
                background: #2d2d2d;
                color: #f0f0e0;
                border: 1px solid #555;
                border-radius: 4px;
                padding: 4px 8px;
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
