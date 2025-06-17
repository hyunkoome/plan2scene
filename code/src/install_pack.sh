#!/usr/bin/env bash
# 설치 실패 시 즉시 중단
set -e

# PyTorch Geometric 설치 스크립트
# CUDA 및 PyTorch 버전 설정
CUDA="cu12.6"
TORCH="2.6.0"

# 캐시 없이 필요한 휠 설치
#pip install --no-cache torch-scatter -f https://pytorch-geometric.com/whl/torch-${TORCH}+${CUDA}.html
#pip install --no-cache torch-sparse  -f https://pytorch-geometric.com/whl/torch-${TORCH}+${CUDA}.html  # 설치에 시간이 다소 걸릴 수 있음 (~30분)
# 필요 시 아래 두 패키지 주석 해제
pip install --no-cache torch-cluster      -f https://pytorch-geometric.com/whl/torch-${TORCH}+${CUDA}.html
pip install --no-cache torch-spline-conv  -f https://pytorch-geometric.com/whl/torch-${TORCH}+${CUDA}.html

#pip install --no-cache torch-geometric