"""多语言翻译模块"""

LANGUAGES = {
    "zh": "中文",
    "en": "English",
    "ja": "日本語",
    "ko": "한국어",
}

_translations = {
    "app_name":      {"zh": "桌面宠物",         "en": "Desktop Pet",        "ja": "デスクトップペット",  "ko": "데스크톱 펫"},
    "feed":          {"zh": "喂食",             "en": "Feed",               "ja": "餌やり",              "ko": "먹이주기"},
    "sleep":         {"zh": "睡觉",             "en": "Sleep",              "ja": "睡眠",                "ko": "잠자기"},
    "wake":          {"zh": "唤醒",             "en": "Wake Up",            "ja": "起こす",              "ko": "깨우기"},
    "quit":          {"zh": "退出",             "en": "Quit",               "ja": "終了",                "ko": "종료"},
    "show_pet":      {"zh": "显示宠物",          "en": "Show Pet",           "ja": "ペットを表示",         "ko": "펫 보이기"},
    "hide_pet":      {"zh": "隐藏宠物",          "en": "Hide Pet",           "ja": "ペットを隠す",         "ko": "펫 숨기기"},
    "coins":         {"zh": "金币",             "en": "Coins",              "ja": "コイン",              "ko": "코인"},
    "hunger":        {"zh": "饱食度",            "en": "Hunger",             "ja": "満腹度",              "ko": "포만감"},
    "happiness":     {"zh": "开心值",            "en": "Happiness",          "ja": "幸福度",              "ko": "행복도"},
    "energy":        {"zh": "精力值",            "en": "Energy",             "ja": "体力",                "ko": "체력"},
    "close":         {"zh": "关闭",             "en": "Close",              "ja": "閉じる",              "ko": "닫기"},
    "buy_and_feed":  {"zh": "购买并喂食",        "en": "Buy & Feed",         "ja": "購入して餌やり",       "ko": "구매 후 먹이기"},
    "settings":      {"zh": "设置",             "en": "Settings",           "ja": "設定",                "ko": "설정"},
    "gift_code":     {"zh": "礼包码",            "en": "Gift Code",          "ja": "ギフトコード",         "ko": "기프트 코드"},
    "redeem":        {"zh": "兑换",             "en": "Redeem",             "ja": "交換",                "ko": "교환"},
    "status":        {"zh": "状态",             "en": "Status",             "ja": "ステータス",           "ko": "상태"},
    "shop":          {"zh": "商店",             "en": "Shop",               "ja": "ショップ",             "ko": "상점"},
    "language":      {"zh": "语言",             "en": "Language",           "ja": "言語",                "ko": "언어"},
    "gift_code_title":    {"zh": "输入礼包码",    "en": "Enter Gift Code",    "ja": "ギフトコード入力",      "ko": "기프트 코드 입력"},
    "gift_code_invalid":  {"zh": "无效的礼包码",  "en": "Invalid gift code",  "ja": "無効なギフトコード",    "ko": "유효하지 않은 코드"},
    "gift_code_success":  {"zh": "获得 {} 金币!", "en": "Got {} coins!",      "ja": "{} コイン獲得！",      "ko": "{} 코인 획득!"},

    # 商店物品
    "item_basic_chip_name":      {"zh": "基础芯片",    "en": "Basic Chip",        "ja": "ベーシックチップ",      "ko": "기본 칩"},
    "item_basic_chip_desc":      {"zh": "基础能源芯片，管饱",  "en": "Basic energy chip, fills you up",  "ja": "基本エネルギーチップ、満腹",  "ko": "기본 에너지 칩, 배부름"},
    "item_crypto_candy_name":    {"zh": "加密糖果",    "en": "Crypto Candy",      "ja": "クリプトキャンディ",     "ko": "크립토 캔디"},
    "item_crypto_candy_desc":    {"zh": "稀有数据糖，吃了超开心",  "en": "Rare data candy, pure joy",  "ja": "レアなデータ飴、超幸せ",  "ko": "희귀 데이터 사탕, 매우 기쁨"},
    "item_cooling_module_name":  {"zh": "散热模块",    "en": "Cooling Module",    "ja": "冷却モジュール",        "ko": "냉각 모듈"},
    "item_cooling_module_desc":  {"zh": "高效散热，稳定运行",  "en": "Efficient cooling, stable runtime",  "ja": "高効率冷却、安定稼働",  "ko": "고효율 냉각, 안정적 작동"},
    "item_energy_core_name":     {"zh": "能量核心",    "en": "Energy Core",       "ja": "エナジーコア",          "ko": "에너지 코어"},
    "item_energy_core_desc":     {"zh": "补充电力，瞬间恢复精力",  "en": "Recharge, instant energy restore",  "ja": "充電、瞬時に体力回復",  "ko": "충전, 즉시 체력 회복"},
    "item_data_fragment_name":   {"zh": "数据碎片",    "en": "Data Fragment",     "ja": "データの欠片",          "ko": "데이터 조각"},
    "item_data_fragment_desc":   {"zh": "珍贵的数据，玩累了但快乐",  "en": "Precious data, tiring but joyful",  "ja": "貴重なデータ、疲れるけど幸せ",  "ko": "귀중한 데이터, 피곤하지만 행복"},
    "item_quantum_coprocessor_name": {"zh": "量子协处理器", "en": "Quantum Coprocessor", "ja": "量子コプロセッサ",    "ko": "양자 코프로세서"},
    "item_quantum_coprocessor_desc": {"zh": "终极升级组件，土豪之选", "en": "Ultimate upgrade, baller choice", "ja": "究極のアップグレード、富豪の選択", "ko": "최종 업그레이드, 부자 선택"},
}

_current_lang = "zh"


def set_language(lang: str):
    global _current_lang
    if lang in LANGUAGES:
        _current_lang = lang


def _(key: str, *args) -> str:
    entry = _translations.get(key, {})
    text = entry.get(_current_lang) if entry else None
    if text is None:
        return key
    if args:
        return text.format(*args)
    return text
