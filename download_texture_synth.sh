#!/usr/bin/env bash
cd ../

set -euo pipefail

# 버전 변수
EMBARK_TEX_SYNTH="texture-synthesis-0.8.2-x86_64-unknown-linux-musl"

# 다운로드 URL prefix
BASE_URL="https://github.com/EmbarkStudios/texture-synthesis/releases/download/0.8.2"

# 설치할 디렉터리
INSTALL_DIR="$EMBARK_TEX_SYNTH"

echo "### Texture Synthesis 바이너리 다운로드 및 압축 해제"
wget "${BASE_URL}/${EMBARK_TEX_SYNTH}.tar.gz" -O "${EMBARK_TEX_SYNTH}.tar.gz"
tar -xf "${EMBARK_TEX_SYNTH}.tar.gz"
rm "${EMBARK_TEX_SYNTH}.tar.gz"

echo "### Seam mask 이미지 다운로드"
mkdir -p "${INSTALL_DIR}"
wget -P "${INSTALL_DIR}" "https://raw.githubusercontent.com/EmbarkStudios/texture-synthesis/main/imgs/masks/1_tile.jpg"

echo "완료: ${INSTALL_DIR} 디렉터리에 바이너리와 마스크가 설치되었습니다."
