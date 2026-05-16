[🇺🇸 English](./README.md) &nbsp;|&nbsp;
[🇨🇳 中文](./README_zh.md) &nbsp;|&nbsp;
[🇯🇵 日本語](./README_ja.md) &nbsp;|&nbsp;
[🇰🇷 한국어](./README_ko.md)

---

# 🤖 데스크톱 펫

**데스크톱에 살고 있는 작은 인터랙티브 픽셀 로봇.**

창문 위에 얹혀 있습니다. 배가 고파집니다. 잠이 듭니다. 제멋대로 돌아다닙니다. 가끔 픽셀 눈으로 멀뚱히 당신을 바라봅니다.

---

## 하는 일

- 투명한 항상 최상위 창으로 화면 위에 머무릅니다 — 타이틀 바도 없고 테두리도 없이 그냥 로봇만 덩그러니
- 배고픔 / 체력 / 행복도가 시간에 따라 줄어드는 소소한 육성 요소
- 심심하면 알아서 돌아다님 (대기 → 걷기 자동 전환)
- 알림도 팝업도 없이 조용히 있다가 — 클릭하면 반짝이며 좋아함

## 기능

- **5가지 픽셀 애니메이션** — 대기(깜빡임), 걷기, 잠자기(ZZZ), 먹기, 기쁨(반짝이는 눈)
- **유한 상태 머신** — 정리된 상태 전이 로직
- **시스템 트레이** — 필요 없을 땐 트레이에 넣어둠
- **속성 시스템** — 포만감 / 행복도 / 체력 감쇠, 코인 수동 획득
- **상점** — 코인으로 음식 구매하여 속성 회복
- **오프라인 보정** — 5분마다 자동 저장, 재접속 시 부재 시간만큼 감쇠 계산
- **클릭 반응** — 한 번 클릭 +5 행복도, 더블클릭 +10
- **드래그 이동** — 잡아서 아무 데나 놓기
- **픽셀 단위 마스크** — 빈 픽셀은 클릭이 통과되어 작업에 방해되지 않음

## 스크린샷

<!-- TODO: 스크린샷 / GIF 추가 -->

*준비 중 — 먼저 찍어서 PR 올려주시면 감사하겠습니다.*

## 빠른 시작

```bash
git clone git@github.com:jiangziyong3-lgtm/desktop-pet.git
cd desktop-pet

python -m venv venv
source venv/bin/activate   # Windows는 `venv\Scripts\activate`

pip install -r requirements.txt
python main.py
```

**요구사항:** Python 3.9+, PySide6 ≥ 6.5.0

## 프로젝트 구조

```
main.py              → 진입점
pet_window.py        → 투명 창, 드래그, 컨텍스트 메뉴, 상태 패널
state_machine.py     → 유한 상태 머신
animator.py          → 프레임 플레이어 (루프 / 단발)
renderer.py          → 픽셀 단위 렌더링 (좌우 반전 지원)
sprites.py           → 16×16 스프라이트 데이터 (팔레트 인덱스)
attributes.py        → 속성 감쇠, 코인 수입, 임계값 트리거
save_manager.py      → JSON 저장 + 오프라인 보정
tray.py              → 시스템 트레이 아이콘 & 메뉴
config.py            → 각종 매개변수 (픽셀 크기, 감쇠율, 팔레트…)
states/              → 상태별 동작 (idle, walk, sleep, eat, happy, drag)
shop/                → 상점 UI & 아이템 정의
```

## 라이선스

MIT — 마음대로 하세요, 로봇한테만 못되게 굴지 말아요.
