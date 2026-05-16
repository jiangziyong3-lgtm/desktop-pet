<style>
  .lang-switch { display: flex; gap: 8px; margin-bottom: 16px; flex-wrap: wrap; }
  .lang-switch label {
    padding: 6px 16px; border: 1px solid #555; border-radius: 6px;
    cursor: pointer; font-size: 14px; transition: all 0.2s;
    user-select: none; background: #1a1a1a; color: #ccc;
  }
  .lang-switch label:hover { border-color: #ff8800; color: #ff8800; }
  .lang-switch input { display: none; }
  .lang-switch input:checked + label { background: #ff8800; color: #1a1a1a; border-color: #ff8800; font-weight: bold; }
  .lang-content { display: none; }
  #lang-zh:checked ~ #content-zh,
  #lang-en:checked ~ #content-en,
  #lang-ja:checked ~ #content-ja,
  #lang-ko:checked ~ #content-ko { display: block; }
</style>

<input type="radio" name="lang" id="lang-zh" checked hidden>
<input type="radio" name="lang" id="lang-en" hidden>
<input type="radio" name="lang" id="lang-ja" hidden>
<input type="radio" name="lang" id="lang-ko" hidden>

<div class="lang-switch">
  <label for="lang-zh">中文</label>
  <label for="lang-en">English</label>
  <label for="lang-ja">日本語</label>
  <label for="lang-ko">한국어</label>
</div>

<!-- ==================== 中文 ==================== -->
<div class="lang-content" id="content-zh">

# 🤖 桌面宠物 — 像素小机器人

一个基于 PySide6 的桌面宠物应用。一只 16×16 像素风小机器人住在你的桌面上，会饿、会困、会开心，你可以拖拽它、喂它、哄它睡觉。

## 功能

- **透明置顶窗口** — 无边框、背景穿透、始终在最前，不影响正常操作
- **像素动画** — 待机(眨眼)、走路、睡觉(ZZZ)、吃东西、开心(星星眼) 5 种动画
- **属性系统** — 饱食度 / 开心值 / 精力值 随时间衰减，被动获取金币
- **状态机** — 有限状态机驱动行为切换，自动从待机进入走路
- **交互方式**
  - 左键拖拽移动 | 单击 (+5开心) | 双击 (+10开心)
  - 右键菜单：喂食 / 睡觉 / 退出
  - 中键：查看属性面板
- **系统托盘** — 常驻托盘图标，支持显示/隐藏/喂食/退出
- **商店系统** — 使用金币购买食物，恢复属性
- **存档系统** — 自动存档(每5分钟)，离线时间补偿

## 安装

```bash
# 克隆仓库
git clone https://github.com/yourname/desktop-pet.git
cd desktop-pet

# 创建虚拟环境（推荐）
python -m venv venv
venv\Scripts\activate   # Windows
# source venv/bin/activate  # macOS / Linux

# 安装依赖
pip install -r requirements.txt

# 运行
python main.py
```

**依赖**: Python 3.9+, PySide6 ≥ 6.5.0

## 架构

```
main.py              → 入口，创建 QApplication / PetWindow / TrayManager
pet_window.py        → 主窗口：透明遮罩、拖拽、右键菜单、状态面板
state_machine.py     → 有限状态机，驱动动画切换和自动行为
animator.py          → 动画播放器：帧切换、循环/非循环模式
renderer.py          → 逐像素渲染（支持水平翻转）
sprites.py           → 16×16 精灵数据 (调色板索引)
attributes.py        → 属性衰减 / 被动金币 / 临界触发
save_manager.py      → JSON 存档 + 离线时间补偿
tray.py              → 系统托盘图标与菜单
config.py            → 所有可调参数 (像素大小/衰减速率/阈值/调色板)
states/              → 各状态逻辑 (idle / walk / sleep / eat / happy / drag)
shop/                → 商店窗口与物品数据
```

## 配置

编辑 `config.py` 可调整所有参数：

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `PIXEL_SIZE` | 6 | 每个像素块的屏幕像素 (16×16→96×96) |
| `TICK_INTERVAL` | 200ms | 状态机 tick 间隔 |
| `HUNGER_CRITICAL` | 10 | 饥饿临界值 (≤10 强制睡觉) |
| `ENERGY_CRITICAL` | 10 | 精力临界值 (≤10 强制睡觉) |
| `WALK_SPEED` | 3 px/tick | 行走速度 |

</div>

<!-- ==================== English ==================== -->
<div class="lang-content" id="content-en">

# 🤖 Desktop Pet — Pixel Robot

A PySide6 desktop pet application. A 16×16 pixel-art robot lives on your desktop — it gets hungry, sleepy, and happy. You can drag it around, feed it, and put it to sleep.

## Features

- **Transparent topmost window** — Frameless, click-through background, always on top
- **Pixel animations** — Idle (blink), Walk, Sleep (ZZZ), Eat, Happy (sparkle eyes) — 5 animations
- **Attribute system** — Hunger / Happiness / Energy decay over time; passive coin income
- **State machine** — FSM-driven behavior with auto-transitions (idle → walk)
- **Interactions**
  - Left drag to move | single click (+5 happiness) | double click (+10)
  - Right-click menu: Feed / Sleep / Quit
  - Middle-click: status panel with progress bars
- **System tray** — Persistent tray icon with show/hide/feed/quit
- **Shop system** — Buy food with coins to restore attributes
- **Save system** — Auto-save every 5 minutes with offline time compensation

## Installation

```bash
git clone https://github.com/yourname/desktop-pet.git
cd desktop-pet

python -m venv venv
venv\Scripts\activate   # Windows
# source venv/bin/activate  # macOS / Linux

pip install -r requirements.txt
python main.py
```

**Requires**: Python 3.9+, PySide6 ≥ 6.5.0

## Architecture

```
main.py              → Entry point: QApplication / PetWindow / TrayManager
pet_window.py        → Main window: transparency mask, drag, context menu, status panel
state_machine.py     → Finite state machine for animation & behavior transitions
animator.py          → Frame player: frame switching, loop / one-shot modes
renderer.py          → Per-pixel renderer with horizontal flip support
sprites.py           → 16×16 sprite data (palette indices)
attributes.py        → Attribute decay / passive coins / critical triggers
save_manager.py      → JSON save + offline time compensation
tray.py              → System tray icon & menu
config.py            → Tunable parameters (pixel size, decay rates, thresholds, palette)
states/              → State logic (idle / walk / sleep / eat / happy / drag)
shop/                → Shop window & item data
```

## Configuration

Edit `config.py` to adjust all parameters:

| Parameter | Default | Description |
|-----------|---------|-------------|
| `PIXEL_SIZE` | 6 | Screen pixels per sprite pixel (16×16 → 96×96) |
| `TICK_INTERVAL` | 200ms | State machine tick interval |
| `HUNGER_CRITICAL` | 10 | Hunger threshold (≤10 forces sleep) |
| `ENERGY_CRITICAL` | 10 | Energy threshold (≤10 forces sleep) |
| `WALK_SPEED` | 3 px/tick | Walk movement speed |

</div>

<!-- ==================== 日本語 ==================== -->
<div class="lang-content" id="content-ja">

# 🤖 デスクトップペット — ドット絵ロボット

PySide6 製のデスクトップペットアプリ。16×16 のドット絵ロボットがデスクトップに住み着き、お腹を空かせたり、眠くなったり、喜んだりします。ドラッグで移動、餌やり、寝かしつけができます。

## 機能

- **透明最前面ウィンドウ** — 枠なし、背景クリック透過、常に最前面
- **ドットアニメーション** — 待機(まばたき)、歩行、睡眠(ZZZ)、食事、喜び(キラキラ目) の5種類
- **属性システム** — 満腹度 / 幸福度 / 体力 が時間経過で減少、コインは受動的獲得
- **ステートマシン** — 有限状態マシンによる動作切替 (待機→歩行の自動遷移)
- **操作方法**
  - 左ドラッグで移動 | シングルクリック (+5幸福度) | ダブルクリック (+10)
  - 右クリックメニュー: 餌やり / 睡眠 / 終了
  - 中クリック: ステータスパネル表示
- **システムトレイ** — 常駐アイコン、表示/非表示/餌やり/終了
- **ショップ** — コインで食べ物を購入し属性を回復
- **セーブ機能** — 5分毎の自動セーブ、オフライン時間補正付き

## インストール

```bash
git clone https://github.com/yourname/desktop-pet.git
cd desktop-pet

python -m venv venv
venv\Scripts\activate   # Windows
# source venv/bin/activate  # macOS / Linux

pip install -r requirements.txt
python main.py
```

**要件**: Python 3.9+, PySide6 ≥ 6.5.0

## アーキテクチャ

```
main.py              → エントリポイント: QApplication / PetWindow / TrayManager
pet_window.py        → メインウィンドウ: 透明マスク、ドラッグ、右クリックメニュー、ステータス
state_machine.py     → 有限状態マシン: アニメーション・行動の遷移制御
animator.py          → フレーム再生: コマ送り、ループ/単発モード
renderer.py          → ピクセル描画 (左右反転対応)
sprites.py           → 16×16 スプライトデータ (パレットインデックス)
attributes.py        → 属性減衰 / 受動コイン / 危険閾値トリガー
save_manager.py      → JSONセーブ + オフライン時間補正
tray.py              → システムトレイアイコンとメニュー
config.py            → 調整可能パラメータ (ピクセルサイズ/減衰率/閾値/パレット)
states/              → 各状態ロジック (idle / walk / sleep / eat / happy / drag)
shop/                → ショップウィンドウとアイテムデータ
```

## 設定

`config.py` で全パラメータを調整可能:

| パラメータ | 既定値 | 説明 |
|-----------|--------|------|
| `PIXEL_SIZE` | 6 | 1ピクセルの画面サイズ (16×16→96×96) |
| `TICK_INTERVAL` | 200ms | ステートマシンの更新間隔 |
| `HUNGER_CRITICAL` | 10 | 空腹閾値 (≤10で強制睡眠) |
| `ENERGY_CRITICAL` | 10 | 体力閾値 (≤10で強制睡眠) |
| `WALK_SPEED` | 3 px/tick | 歩行速度 |

</div>

<!-- ==================== 한국어 ==================== -->
<div class="lang-content" id="content-ko">

# 🤖 데스크톱 펫 — 픽셀 로봇

PySide6 기반 데스크톱 펫 애플리케이션. 16×16 픽셀 아트 로봇이 데스크톱에 살면서 배고파하고, 졸려하고, 기뻐합니다. 드래그로 이동시키고, 먹이를 주고, 재울 수 있습니다.

## 기능

- **투명 최상위 창** — 테두리 없음, 배경 클릭 투과, 항상 맨 위에 표시
- **픽셀 애니메이션** — 대기(깜빡임), 걷기, 잠자기(ZZZ), 먹기, 기쁨(반짝이는 눈) 5종
- **속성 시스템** — 포만감 / 행복도 / 체력이 시간에 따라 감소, 코인 수동 획득
- **상태 머신** — FSM 기반 행동 전환 (대기→걷기 자동 전환)
- **조작 방법**
  - 왼쪽 드래그로 이동 | 클릭 (+5 행복도) | 더블클릭 (+10)
  - 우클릭 메뉴: 먹이주기 / 잠자기 / 종료
  - 중간 클릭: 상태 패널 표시
- **시스템 트레이** — 상주 아이콘, 표시/숨기기/먹이/종료
- **상점** — 코인으로 음식을 구매하여 속성 회복
- **저장 시스템** — 5분마다 자동 저장, 오프라인 시간 보정

## 설치

```bash
git clone https://github.com/yourname/desktop-pet.git
cd desktop-pet

python -m venv venv
venv\Scripts\activate   # Windows
# source venv/bin/activate  # macOS / Linux

pip install -r requirements.txt
python main.py
```

**요구사항**: Python 3.9+, PySide6 ≥ 6.5.0

## 아키텍처

```
main.py              → 진입점: QApplication / PetWindow / TrayManager
pet_window.py        → 메인 윈도우: 투명 마스크, 드래그, 우클릭 메뉴, 상태 패널
state_machine.py     → 유한 상태 머신: 애니메이션 및 행동 전환 제어
animator.py          → 프레임 플레이어: 프레임 전환, 루프/단발 모드
renderer.py          → 픽셀 단위 렌더링 (좌우 반전 지원)
sprites.py           → 16×16 스프라이트 데이터 (팔레트 인덱스)
attributes.py        → 속성 감소 / 수동 코인 / 임계값 트리거
save_manager.py      → JSON 저장 + 오프라인 시간 보정
tray.py              → 시스템 트레이 아이콘 및 메뉴
config.py            → 조정 가능한 매개변수 (픽셀 크기/감소율/임계값/팔레트)
states/              → 각 상태 로직 (idle / walk / sleep / eat / happy / drag)
shop/                → 상점 창과 아이템 데이터
```

## 설정

`config.py`에서 모든 매개변수 조정 가능:

| 매개변수 | 기본값 | 설명 |
|---------|--------|------|
| `PIXEL_SIZE` | 6 | 픽셀 블록의 화면 픽셀 크기 (16×16→96×96) |
| `TICK_INTERVAL` | 200ms | 상태 머신 틱 간격 |
| `HUNGER_CRITICAL` | 10 | 배고픔 임계값 (≤10 강제 수면) |
| `ENERGY_CRITICAL` | 10 | 체력 임계값 (≤10 강제 수면) |
| `WALK_SPEED` | 3 px/tick | 걷기 속도 |

</div>
