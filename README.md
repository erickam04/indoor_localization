# BLE Indoor Localization

BLE 비컨의 RSSI로 실내 위치를 추정하는 과정을 Python으로 구현한 시뮬레이션 프로젝트입니다. 장애물과 신호 잡음이 있는 공간에서 **Trilateration과 Fingerprinting의 추정 결과가 어떻게 달라지는지** 비교하고, 이동 경로에 smoothing을 적용해봤습니다.

## 프로젝트 소개

실내에서는 같은 거리에서도 장애물과 잡음에 따라 RSSI가 달라질 수 있습니다. 이를 간단한 환경으로 모델링하고, RSSI를 거리로 바꾸는 방식과 위치별 신호 패턴을 비교하는 방식을 함께 구현했습니다.

실제 BLE 장비로 데이터를 수집하는 대신, 경로 손실·벽 감쇠·Gaussian noise를 반영한 RSSI를 생성해 사용했습니다.

## 구현한 내용

| 구성 | 방식 |
|---|---|
| **Trilateration** | RSSI를 거리로 변환하고 비선형 최소제곱법으로 위치 추정 |
| **Fingerprinting** | 격자별 RSSI radio map을 만들고 거리 가중 k-NN으로 위치 추정 |
| **Trajectory smoothing** | 추정 좌표에 이동평균 또는 지수이동평균 적용 |
| **Visualization** | 비컨·벽·실제 위치와 추정 위치, 이동 경로 비교 |

## 시뮬레이션 설정

기본 환경은 **10 × 10 m 공간과 모서리에 배치한 비컨 4개**입니다. Fingerprinting은 1 m 간격의 격자에서 위치마다 RSSI를 10회 측정해 평균을 내고, `k=3`을 사용합니다.

비컨과 벽 배치, 잡음 크기, 격자 간격, 이동 경로와 필터 설정은 [config.py](BLE_indoor_localization/config.py)에서 바꿀 수 있습니다.

## 비교 방법

- **단일 위치:** 실제 위치와 추정 위치 사이의 거리 오차를 출력하고 그림으로 표시합니다.
- **이동 경로:** 두 알고리즘에 같은 RSSI를 입력하고, smoothing을 적용한 경로와 평균 위치 오차를 비교합니다.

경로 실험에서 출력하는 `MAE`는 각 시점의 2차원 위치 거리 오차를 평균한 값(m)입니다. 실행마다 잡음을 새로 생성하므로 결과는 달라질 수 있습니다.

## 실행 방법

Python 3.10 이상이 필요합니다. 저장소 루트에서 의존성을 설치한 뒤 실행합니다.

```bash
python -m pip install numpy scipy scikit-learn matplotlib
cd BLE_indoor_localization
```

원하는 실험을 하나씩 실행하면 오차가 터미널에 출력되고 그래프 창이 열립니다.

```bash
python test_tri.py           # Trilateration 단일 위치 추정
python test_fingerprint.py   # Fingerprinting 단일 위치 추정
python test_trajectory.py    # 이동 경로와 smoothing 비교
```

`test_*.py`는 시뮬레이션 실행 스크립트입니다. 기본 경로 실험은 이동평균을 사용하며, `FILTER_CONFIG`에서 지수이동평균으로 변경할 수 있습니다.

## Repository Structure

```text
BLE_indoor_localization/
├── config.py              # 환경과 실험 설정
├── alg/
│   ├── trilateration.py
│   ├── fingerprinting.py
│   └── smoothing.py
├── sim/
│   ├── env.py             # RSSI 생성
│   └── obstacles.py       # 벽과 신호 경로의 교차 판정
├── test_tri.py
├── test_fingerprint.py
└── test_trajectory.py
```

## 한계

단순화한 2차원 시뮬레이션으로, 실제 BLE 장비의 정확도를 측정한 결과는 아닙니다. Fingerprinting의 radio map 생성과 평가에는 같은 환경 모델을 사용했습니다. 실제 공간에서의 다중경로, 기기별 편차, 환경 변화에 대한 검증이 더 필요합니다.
