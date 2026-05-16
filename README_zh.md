[🇺🇸 English](./README.md) &nbsp;|&nbsp;
[🇨🇳 中文](./README_zh.md) &nbsp;|&nbsp;
[🇯🇵 日本語](./README_ja.md) &nbsp;|&nbsp;
[🇰🇷 한국어](./README_ko.md)

---

# 🤖 桌面宠物

**一只住在你桌面上的交互式像素小机器人。**

它挂在所有窗口之上。会饿。会睡着。会自己溜达。偶尔像素眼一眨一眨地看着你，满脸无所谓。

---

## 它能干嘛

- 以一个透明置顶窗口的形式待在你屏幕上——没有标题栏、没有边框，就是机器人本体
- 有真实的生存需求：饱食度会掉、精力会耗、不理它的话开心值也会降
- 无聊了会自己到处走（待机 → 走路自动切换）
- 不吵不闹不弹通知——但戳它一下，它会开心得冒星星

## 功能

- **7 种像素动画** — 待机（眨眼）、沮丧待机、开心待机、走路、睡觉（躺倒+ZZZ）、吃东西、开心（星星眼）
- **心情影响待机** — 开心值 <30 沮丧脸 / 30-70 正常 / >70 笑眯眯
- **有限状态机** — 状态切换干净利落，逻辑一目了然
- **系统托盘** — 不打扰你的时候缩在托盘里
- **四国语言** — 中文 / English / 日本語 / 한국어，设置中一键切换
- **属性系统** — 饱食度 / 开心值 / 精力值随时间衰减，金币被动获取
- **内置商店** — 用金币买食物恢复属性
- **离线补偿** — 每 5 分钟自动存档，重新打开时自动计算离线衰减
- **点击交互** — 单击 +5 开心值，双击 +10
- **拖拽移动** — 按住就拖，松手就停
- **像素级遮罩** — 空白像素不拦截点击，不影响你干正事

## 截图

<!-- TODO: 补几张截图或 GIF -->

*还没截，欢迎 PR 来补。*

## 快速开始

```bash
git clone git@github.com:jiangziyong3-lgtm/desktop-pet.git
cd desktop-pet

python -m venv venv
source venv/bin/activate   # Windows 用 `venv\Scripts\activate`

pip install -r requirements.txt
python main.py
```

**环境要求：** Python 3.9+, PySide6 ≥ 6.5.0

## 项目结构

```
main.py              → 入口 + 语言初始化
pet_window.py        → 透明窗口、拖拽、右键菜单、状态面板
state_machine.py     → 有限状态机
animator.py          → 动画播放器（循环/单次）
renderer.py          → 逐像素渲染（支持水平翻转）
sprites.py           → 16×16 精灵数据（7 种动画）
attributes.py        → 属性衰减、金币收益、临界触发
save_manager.py      → JSON 存档 + 离线补偿
tray.py              → 系统托盘图标与菜单
config.py            → 所有可调参数（像素大小、衰减速率、调色板……）
i18n.py              → 多语言翻译系统（中/英/日/韩）
settings_window.py   → 设置界面（语言切换）
states/              → 各状态行为（idle, walk, sleep, eat, happy, drag）
shop/                → 商店 UI 与物品定义
```

## 许可证

MIT — 随便玩，别欺负机器人就行。
