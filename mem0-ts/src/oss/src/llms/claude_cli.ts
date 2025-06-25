import { exec } from 'child_process';
import { promisify } from 'util';
import { BaseLLMConfig } from '../config/types';
import { LLMBase } from './base';

const execAsync = promisify(exec);

export class ClaudeCLILLM extends LLMBase {
  private modelMap: Record<string, string> = {
    'opus': 'opus',
    'claude-opus': 'opus', 
    'claude-4-opus': 'opus',
    'sonnet': 'sonnet',
    'claude-sonnet': 'sonnet',
    'claude-4-sonnet': 'sonnet'
  };

  constructor(config?: BaseLLMConfig) {
    super(config);
    
    // 기본 모델 설정
    if (!this.config.model) {
      this.config.model = 'sonnet';
    }
  }

  private formatMessagesForClaude(messages: Array<{ role: string; content: string }>): string {
    const formatted: string[] = [];
    
    for (const msg of messages) {
      const role = msg.role || 'user';
      const content = msg.content || '';
      
      if (role === 'system') {
        formatted.push(`System: ${content}`);
      } else if (role === 'user') {
        formatted.push(`Human: ${content}`);
      } else if (role === 'assistant') {
        formatted.push(`Assistant: ${content}`);
      }
    }
    
    return formatted.join('\n\n');
  }

  async generateResponse(
    messages: Array<{ role: string; content: string }>,
    options?: {
      response_format?: any;
      tools?: any[];
      tool_choice?: string;
    }
  ): Promise<string> {
    // 메시지 형식화
    const prompt = this.formatMessagesForClaude(messages);
    
    // Claude CLI 모델 이름
    const modelName = this.modelMap[this.config.model] || 'sonnet';
    
    // Claude CLI 명령어 구성
    const maxTokens = this.config.max_tokens || 2000;
    let cmd = `claude chat --model ${modelName} --max-tokens ${maxTokens}`;
    
    // 온도 설정
    if (this.config.temperature !== undefined) {
      cmd += ` --temperature ${this.config.temperature}`;
    }
    
    try {
      // Claude CLI 실행
      const { stdout, stderr } = await execAsync(cmd, {
        env: { ...process.env },
        maxBuffer: 1024 * 1024 * 10 // 10MB buffer
      });
      
      if (stderr) {
        console.warn('Claude CLI warning:', stderr);
      }
      
      return stdout.trim();
      
    } catch (error: any) {
      if (error.code === 'ENOENT') {
        throw new Error(
          'Claude CLI not found. Please install it with: npm install -g @anthropic-ai/claude-code'
        );
      }
      throw new Error(`Claude CLI error: ${error.message}`);
    }
  }
}