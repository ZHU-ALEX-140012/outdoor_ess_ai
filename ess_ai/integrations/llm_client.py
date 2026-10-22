"""DeepSeek OpenAI-compatible 客户端。

默认离线：没有密钥或 ``project.mode=offline`` 时不会发起网络请求，而是返回
调用方提供的 fallback。这样演示、测试与 CI 不依赖任何外部服务。
"""

from __future__ import annotations

import os
import time
from dataclasses import dataclass, field
from typing import Any

import utils
from ess_ai.config import Settings

logger = utils.get_logger(__name__)


class LLMError(RuntimeError):
    """大模型调用失败。"""


@dataclass(frozen=True)
class LLMResult:
    """一次补全结果，附带可审计的元信息。"""

    text: str
    model: str
    provider: str = "deepseek"
    offline: bool = False
    usage: dict[str, Any] = field(default_factory=dict)
    error: str | None = None


class DeepSeekClient:
    """最小封装：仅暴露聊天补全，避免业务层耦合 SDK 细节。"""

    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.model = str(settings.get("llm.model", "deepseek-v4.1-flash"))
        self.base_url = str(
            os.getenv("DEEPSEEK_BASE_URL")
            or settings.get("llm.base_url", "https://api.deepseek.com/v1")
        )
        self.api_key_env = str(settings.get("llm.api_key_env", "DEEPSEEK_API_KEY"))
        self.api_key = os.getenv(self.api_key_env, "").strip()
        self.temperature = float(settings.get("llm.temperature", 0.3))
        self.max_tokens = int(settings.get("llm.max_tokens", 4096))
        self.timeout = float(settings.get("llm.timeout_seconds", 60))
        self.max_retries = max(0, int(settings.get("llm.max_retries", 3)))
        self.offline_fallback = bool(settings.get("llm.offline_fallback", True))

    @property
    def configured(self) -> bool:
        """是否具备发起真实请求的条件。"""

        return bool(self.api_key) and not self.settings.is_offline

    def complete(
        self,
        system_prompt: str,
        user_prompt: str,
        *,
        fallback: str = "",
        temperature: float | None = None,
        json_mode: bool = False,
    ) -> LLMResult:
        """执行一次聊天补全；离线或失败时按配置回退。"""

        if not self.configured:
            return LLMResult(
                text=fallback,
                model=self.model,
                offline=True,
                error=None if not self.api_key else "project.mode=offline",
            )

        try:
            from openai import OpenAI  # type: ignore[import-not-found]
        except ImportError as exc:
            return self._fallback(fallback, f"openai SDK 未安装: {exc}")

        kwargs: dict[str, Any] = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "temperature": self.temperature if temperature is None else float(temperature),
            "max_tokens": self.max_tokens,
        }
        if json_mode:
            kwargs["response_format"] = {"type": "json_object"}

        last_error: str | None = None
        for attempt in range(self.max_retries + 1):
            try:
                client = OpenAI(
                    api_key=self.api_key,
                    base_url=self.base_url,
                    timeout=self.timeout,
                    max_retries=0,
                )
                response = client.chat.completions.create(**kwargs)
                text = ""
                if response.choices:
                    text = response.choices[0].message.content or ""
                usage: dict[str, Any] = {}
                raw_usage = getattr(response, "usage", None)
                if raw_usage is not None:
                    usage = (
                        raw_usage.model_dump()
                        if hasattr(raw_usage, "model_dump")
                        else dict(raw_usage)
                    )
                if not text.strip():
                    raise LLMError("模型返回空内容")
                return LLMResult(
                    text=text.strip(),
                    model=self.model,
                    usage=usage,
                )
            except Exception as exc:  # SDK 异常类型随版本变化，统一兜底
                last_error = f"{type(exc).__name__}: {exc}"
                logger.warning(
                    "DeepSeek 调用失败（第 %d/%d 次）: %s",
                    attempt + 1,
                    self.max_retries + 1,
                    last_error,
                )
                if attempt < self.max_retries:
                    time.sleep(min(2**attempt, 8))

        if self.offline_fallback:
            return self._fallback(fallback, last_error)
        raise LLMError(f"DeepSeek 调用失败: {last_error}")

    def _fallback(self, fallback: str, error: str | None) -> LLMResult:
        if not self.offline_fallback:
            raise LLMError(error or "模型不可用")
        return LLMResult(text=fallback, model=self.model, offline=True, error=error)

    def read_prompt(self, name: str) -> str:
        """从 ``prompts/`` 读取提示词模板。"""

        prompt_dir = self.settings.path("paths.prompts_dir")
        return utils.read_text(prompt_dir / name)
