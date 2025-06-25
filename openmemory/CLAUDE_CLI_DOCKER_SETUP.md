# Claude-Code CLI 도커 실행 가이드

## 🎯 Claude-Code CLI를 도커에서 사용하기

### 1️⃣ **사전 준비 (호스트에서)**

```bash
# Claude CLI 설치 (아직 안했다면)
npm install -g @anthropic-ai/claude-code

# Claude 로그인 (중요!)
claude login
# 브라우저에서 Anthropic 계정으로 로그인

# 로그인 확인
ls ~/.claude/
# config.json 파일이 있어야 함
```

### 2️⃣ **환경 설정**

```bash
cd /Users/kanghyeonlee/Dev/leekh/mem0/openmemory

# .env 파일 생성
cat > api/.env << EOF
OPENAI_API_KEY=sk-your-openai-key-here  # 임베딩용
USER=your-username
NEXT_PUBLIC_API_URL=http://localhost:8765
EOF
```

### 3️⃣ **도커 실행**

```bash
# Claude CLI 도커 컴포즈로 실행
docker-compose -f docker-compose.claude-cli.yml up --build
```

### 4️⃣ **인증 확인 및 문제 해결**

#### ✅ **성공 시**
```
✅ Claude CLI 인증 확인됨
INFO:     Started server process
INFO:     Uvicorn running on http://0.0.0.0:8765
```

#### ❌ **인증 실패 시**
```
❌ Claude CLI 인증이 필요합니다.
호스트에서 다음 명령을 실행하세요:
  claude login
```

**해결 방법:**
```bash
# 1. 호스트에서 로그인 확인
claude login

# 2. 인증 파일 확인
ls -la ~/.claude/
# config.json이 있는지 확인

# 3. 도커 재시작
docker-compose -f docker-compose.claude-cli.yml restart
```

### 5️⃣ **서비스 접속**

- **🚀 API 서버**: http://localhost:8765
- **🌐 Web UI**: http://localhost:3000
- **🗄️ Qdrant**: http://localhost:6333

### 6️⃣ **테스트**

```bash
# API 테스트
curl -X POST http://localhost:8765/v1/memories \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [{"role": "user", "content": "안녕하세요"}],
    "user_id": "test_user"
  }'
```

## 🔧 **고급 설정**

### 인증 파일 수동 복사 (필요시)
```bash
# 컨테이너 실행 중일 때
docker ps  # 컨테이너 ID 확인
docker cp ~/.claude/. <container_id>:/root/.claude/
docker restart <container_id>
```

### 로그 확인
```bash
# 실시간 로그 확인
docker-compose -f docker-compose.claude-cli.yml logs -f openmemory-claude-cli

# Claude CLI 테스트
docker exec -it <container_id> claude --version
```

## ⚠️ **주의사항**

1. **인증 필수**: 호스트에서 `claude login` 필수
2. **인증 만료**: 주기적으로 재로그인 필요할 수 있음
3. **권한**: `~/.claude` 폴더 읽기 권한 필요
4. **네트워크**: Claude CLI는 인터넷 연결 필요

## 💰 **비용 구성**

- **LLM**: Claude-Code CLI (유료 구독 활용)
- **임베딩**: OpenAI API (저렴함, 월 수백원)
- **벡터 DB**: Qdrant (무료)

## 🎉 **완료!**

이제 유료 Claude-Code CLI를 도커에서 사용할 수 있습니다!
기존 구독을 최대한 활용하면서 컨테이너화된 환경에서 mem0를 실행하세요.