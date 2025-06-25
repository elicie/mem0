import json
import subprocess
from typing import Dict, List, Optional

from mem0.configs.llms.base import BaseLlmConfig
from mem0.llms.base import LLMBase


class ClaudeCLILLM(LLMBase):
    def __init__(self, config: Optional[BaseLlmConfig] = None):
        super().__init__(config)
        
        # Claude CLI에서 사용 가능한 모델
        # opus: Claude 4 Opus (가장 강력함)
        # sonnet: Claude 4 Sonnet (균형잡힌 성능)
        if not self.config.model:
            self.config.model = "sonnet"
            
        # 모델 이름 매핑
        self.model_map = {
            "opus": "opus",
            "claude-opus": "opus",
            "claude-4-opus": "opus",
            "sonnet": "sonnet", 
            "claude-sonnet": "sonnet",
            "claude-4-sonnet": "sonnet"
        }
        
    def _format_messages_for_claude(self, messages: List[Dict[str, str]]) -> str:
        """Claude CLI 형식으로 메시지 변환"""
        formatted = []
        for msg in messages:
            role = msg.get("role", "user")
            content = msg.get("content", "")
            
            if role == "system":
                # Claude CLI는 시스템 프롬프트를 첫 번째 유저 메시지에 포함
                formatted.append(f"System: {content}")
            elif role == "user":
                formatted.append(f"Human: {content}")
            elif role == "assistant":
                formatted.append(f"Assistant: {content}")
                
        return "\n\n".join(formatted)
    
    def _parse_response(self, response: str, tools: Optional[List[Dict]] = None) -> str:
        """응답 파싱"""
        # 툴 콜이 있는 경우 처리 (현재는 기본 텍스트 응답만 지원)
        if tools:
            # 추후 툴 지원 구현 시 확장
            return response
        return response
        
    def generate_response(
        self,
        messages: List[Dict[str, str]],
        response_format=None,
        tools: Optional[List[Dict]] = None,
        tool_choice: str = "auto",
    ):
        """
        Claude CLI를 사용하여 응답 생성
        
        Args:
            messages (list): 메시지 목록
            response_format: 응답 형식 (현재 미지원)
            tools (list, optional): 툴 목록 (현재 미지원)
            tool_choice (str, optional): 툴 선택 방법
            
        Returns:
            str: 생성된 응답
        """
        # 메시지 형식화
        prompt = self._format_messages_for_claude(messages)
        
        # Claude CLI 모델 이름 가져오기
        model_name = self.model_map.get(self.config.model, "sonnet")
        
        # Claude CLI 명령어 구성
        cmd = [
            "claude",
            "chat",
            "--model", model_name,
            "--max-tokens", str(self.config.max_tokens or 2000),
        ]
        
        # 온도 설정 (Claude CLI가 지원하는 경우)
        if self.config.temperature is not None:
            cmd.extend(["--temperature", str(self.config.temperature)])
            
        try:
            # Claude CLI 실행
            result = subprocess.run(
                cmd,
                input=prompt,
                text=True,
                capture_output=True,
                check=True
            )
            
            response = result.stdout.strip()
            
            # 응답 파싱
            return self._parse_response(response, tools)
            
        except subprocess.CalledProcessError as e:
            error_msg = f"Claude CLI error: {e.stderr}"
            raise RuntimeError(error_msg) from e
        except FileNotFoundError:
            raise RuntimeError(
                "Claude CLI not found. Please install it with: npm install -g @anthropic-ai/claude-code"
            )