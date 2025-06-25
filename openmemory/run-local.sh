#!/bin/bash

echo "=== mem0 로컬 실행 스크립트 ==="
echo "Claude CLI와 함께 로컬에서 실행합니다."

# 환경 확인
echo "환경 확인 중..."
if ! command -v claude &> /dev/null; then
    echo "❌ Claude CLI가 설치되지 않았습니다."
    echo "설치: npm install -g @anthropic-ai/claude-code"
    exit 1
fi

if ! command -v python &> /dev/null; then
    echo "❌ Python이 설치되지 않았습니다."
    exit 1
fi

echo "✅ Claude CLI: $(claude --version 2>/dev/null || echo '설치됨')"
echo "✅ Python: $(python --version)"

# 현재 디렉토리를 API 폴더로 변경
cd "$(dirname "$0")/api"

# .env 파일 확인
if [ ! -f .env ]; then
    echo "❌ .env 파일이 없습니다."
    echo "다음 내용으로 .env 파일을 생성하세요:"
    echo "OPENAI_API_KEY=sk-your-openai-key"
    echo "USER=your-username"
    exit 1
fi

# Python 의존성 설치
echo "Python 의존성 설치 중..."
pip install -r requirements.txt

# Qdrant 시작 (도커로)
echo "Qdrant 벡터 데이터베이스 시작 중..."
docker run -d --name mem0-qdrant -p 6333:6333 -v mem0_storage:/qdrant/storage qdrant/qdrant 2>/dev/null || echo "Qdrant 이미 실행 중"

# API 서버 시작
echo "🚀 mem0 API 서버 시작..."
echo "접속 주소: http://localhost:8765"
python -m uvicorn main:app --host 0.0.0.0 --port 8765 --reload