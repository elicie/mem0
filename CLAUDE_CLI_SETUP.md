# Claude CLI + OpenAI 임베딩 하이브리드 설정 가이드

## 개요
이 가이드는 LLM은 Claude CLI로, 임베딩은 OpenAI API로 사용하는 하이브리드 설정을 설명합니다.

## 사전 요구사항

### 1. Claude CLI 설치
```bash
# Claude CLI 전역 설치
npm install -g @anthropic-ai/claude-code

# Claude 계정으로 로그인
claude login
```

### 2. OpenAI API 키 설정
```bash
# 환경변수 설정 (Linux/Mac)
export OPENAI_API_KEY="your-openai-api-key-here"

# 또는 .env 파일에 추가
echo "OPENAI_API_KEY=your-openai-api-key-here" >> .env
```

## 설정

### 1. 기본 설정 (하이브리드 방식)
`openmemory/api/default_config.json`:
```json
{
    "mem0": {
        "llm": {
            "provider": "claude_cli",
            "config": {
                "model": "sonnet",
                "temperature": 0.1,
                "max_tokens": 2000
            }
        },
        "embedder": {
            "provider": "openai",
            "config": {
                "model": "text-embedding-3-small",
                "api_key": "env:OPENAI_API_KEY"
            }
        }
    }
}
```

### 2. 프로그래밍 방식 설정
```python
from mem0 import Memory

# Claude CLI LLM + OpenAI 임베딩 하이브리드
config = {
    "llm": {
        "provider": "claude_cli",
        "config": {
            "model": "sonnet",  # 또는 "opus"
            "temperature": 0.1,
            "max_tokens": 2000
        }
    },
    "embedder": {
        "provider": "openai",
        "config": {
            "model": "text-embedding-3-small",  # 또는 "text-embedding-3-large"
            "api_key": "your-openai-api-key"
        }
    }
}

m = Memory(config=config)
```

## 사용 가능한 모델

### Claude CLI 모델
- `sonnet`: Claude 4 Sonnet (균형잡힌 성능, 권장)
- `opus`: Claude 4 Opus (가장 강력함)

### OpenAI 임베딩 모델
- `text-embedding-3-small` (기본값, 저렴하고 빠름, $0.00002/1K 토큰)
- `text-embedding-3-large` (고품질, $0.00013/1K 토큰)
- `text-embedding-ada-002` (이전 모델, 호환성용)

## 하이브리드 방식의 장점

1. **LLM 비용 절약**: Claude CLI로 LLM 비용 완전 제거
2. **최적의 임베딩**: OpenAI의 검증된 고품질 임베딩
3. **빠른 속도**: 네트워크 임베딩으로 CPU 부담 없음
4. **저렴한 임베딩 비용**: 월 수십원~수백원 수준
5. **안정성**: 업계 표준 OpenAI 임베딩 사용

## 제한사항

1. **이미지 지원 없음**: Claude CLI는 현재 이미지를 지원하지 않음
2. **툴 호출 제한**: 기본적인 텍스트 생성만 지원
3. **OpenAI API 키 필요**: 임베딩을 위한 OpenAI API 키 필요
4. **네트워크 의존**: 임베딩 처리 시 인터넷 연결 필요

## 문제 해결

### Claude CLI를 찾을 수 없음
```bash
# Claude CLI가 설치되어 있는지 확인
which claude

# 재설치
npm install -g @anthropic-ai/claude-code
```

### OpenAI API 키 오류
```bash
# API 키가 설정되었는지 확인
echo $OPENAI_API_KEY

# API 키 테스트
curl -H "Authorization: Bearer $OPENAI_API_KEY" \
  https://api.openai.com/v1/models
```

## 예제

```python
from mem0 import Memory

# 하이브리드 Memory 인스턴스 생성 (기본 설정 사용)
m = Memory()

# 메모리 추가 (Claude CLI로 처리 + OpenAI 임베딩)
m.add("나는 파이썬을 좋아한다", user_id="user1")

# 메모리 검색 (OpenAI 임베딩으로 유사성 검색)
results = m.search("프로그래밍 언어", user_id="user1")
print(results)

# 비용 효율적: LLM은 무료(Claude CLI), 임베딩은 저렴(OpenAI)
```

## 비용 분석

```
월간 예상 비용 (임베딩만):
- 개인 사용: $0.001-0.01 (약 1-14원)
- 중간 사용: $0.01-0.1 (약 14-140원)
- 대량 사용: $0.1-1.0 (약 140-1400원)

LLM 비용: $0 (Claude CLI 사용)
총 비용: 기존 OpenAI 전체 사용 대비 90% 이상 절약
```