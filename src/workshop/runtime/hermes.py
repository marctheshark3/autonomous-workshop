"""Bounded structured-output calls through Hermes Agent."""

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Any, Mapping, Optional

from workshop.errors import ContractError
from workshop.runtime.codex import (
    DEFAULT_CODEX_TIMEOUT_SECONDS,
    MAX_CODEX_OUTPUT_BYTES,
    CodexInvocationError,
)
from workshop.runtime.engine import DEFAULT_HERMES_PROVIDER
from workshop.runtime.execution import hermes_subprocess_environment


_REASONING_LEVELS = {
    "low": "low",
    "medium": "medium",
    "high": "high",
    "xhigh": "xhigh",
}


class HermesStructuredRunner:
    def __init__(
        self,
        *,
        model: str,
        reasoning_effort: str,
        binary: Optional[str] = None,
        timeout_seconds: int = DEFAULT_CODEX_TIMEOUT_SECONDS,
        runner: Any = subprocess.run,
        cli_version: Optional[str] = None,
        provider: Optional[str] = None,
    ) -> None:
        if not isinstance(model, str) or not model.strip() or len(model) > 128:
            raise ContractError("Workshop Hermes model must be a bounded identifier")
        if reasoning_effort not in _REASONING_LEVELS:
            raise ValueError("unsupported Hermes reasoning effort")
        if type(timeout_seconds) is not int or not 1 <= timeout_seconds <= 3_600:
            raise ValueError("Hermes timeout_seconds must be from 1 to 3,600")
        self.binary = (
            binary or os.environ.get("WORKSHOP_HERMES_BIN") or shutil.which("hermes")
        )
        self.model = model.strip()
        self.provider = (
            provider
            or os.environ.get("WORKSHOP_HERMES_PROVIDER")
            or DEFAULT_HERMES_PROVIDER
        )
        self.reasoning_effort = reasoning_effort
        self.timeout_seconds = timeout_seconds
        self._runner = runner
        self.cli_version = cli_version or self._read_cli_version()
        self.last_used_web_search = False

    def _read_cli_version(self) -> str:
        if not self.binary:
            return "0.0.0"
        try:
            completed = self._runner(
                [self.binary, "--version"],
                capture_output=True,
                text=True,
                timeout=10,
                check=False,
                env=hermes_subprocess_environment(),
            )
        except (OSError, subprocess.SubprocessError):
            return "0.0.0"
        output = completed.stdout if isinstance(completed.stdout, str) else ""
        match = re.search(r"\d+(?:\.\d+){1,3}(?:[-+][A-Za-z0-9.-]+)?", output)
        return match.group(0) if match else "0.0.0"

    def invoke(
        self,
        *,
        prompt: str,
        schema: Mapping[str, Any],
        workspace: Optional[Path] = None,
        native_web_search: bool = False,
    ) -> Mapping[str, Any]:
        if not self.binary:
            raise CodexInvocationError("Hermes CLI is not installed or on PATH")
        if type(native_web_search) is not bool:
            raise ValueError("native_web_search must be a boolean")

        self.last_used_web_search = False
        remaining = self.timeout_seconds
        try:
            completed = self._run_attempt(
                prompt=prompt,
                schema=schema,
                workspace=workspace,
                native_web_search=native_web_search,
                timeout_seconds=float(remaining),
            )
        except subprocess.TimeoutExpired as exc:
            exc.output = None
            exc.stderr = None
            raise CodexInvocationError("Hermes structured call timed out") from None
        except (OSError, subprocess.SubprocessError, TypeError, ValueError):
            raise CodexInvocationError(
                "Hermes could not execute the structured call"
            ) from None

        stdout = completed.stdout if isinstance(completed.stdout, str) else ""
        if completed.returncode != 0:
            raise CodexInvocationError("Hermes did not complete the structured call")
        payload = _decode_json_object(stdout)
        self.last_used_web_search = native_web_search
        return payload

    def _run_attempt(
        self,
        *,
        prompt: str,
        schema: Mapping[str, Any],
        workspace: Optional[Path],
        native_web_search: bool,
        timeout_seconds: float,
    ):
        with tempfile.TemporaryDirectory(prefix="workshop-hermes-") as temporary:
            control_root = Path(temporary)
            query_path = control_root / "query.txt"
            wrapped = (
                "Return only JSON matching this schema. No markdown.\nSCHEMA:\n"
                + json.dumps(schema, sort_keys=True)
                + "\n\nPROMPT:\n"
                + prompt
            )
            query_path.write_text(wrapped, encoding="utf-8")
            cwd = Path(workspace).resolve() if workspace is not None else control_root
            cwd.mkdir(parents=True, exist_ok=True)
            command = [
                self.binary,
                "chat",
                "--query-file",
                str(query_path),
                "-Q",
                "--ignore-rules",
                "--yolo",
                "--provider",
                self.provider,
                "-m",
                self.model,
                "--reasoning",
                _REASONING_LEVELS[self.reasoning_effort],
                "--in",
                str(cwd),
            ]
            if not native_web_search:
                command.extend(("--toolsets", "file"))
            return self._runner(
                command,
                capture_output=True,
                text=True,
                timeout=timeout_seconds,
                check=False,
                env=hermes_subprocess_environment(),
            )


def _decode_json_object(text: str) -> Mapping[str, Any]:
    if not text or len(text.encode("utf-8")) > MAX_CODEX_OUTPUT_BYTES:
        raise CodexInvocationError("Hermes returned no valid structured result")
    stripped = text.strip()
    candidates = [stripped]
    fenced = re.search(r"```(?:json)?\s*(\{.*\})\s*```", stripped, re.DOTALL)
    if fenced:
        candidates.insert(0, fenced.group(1))
    start = stripped.find("{")
    end = stripped.rfind("}")
    if start >= 0 and end > start:
        candidates.insert(0, stripped[start : end + 1])
    for candidate in candidates:
        try:
            payload = json.loads(candidate)
        except ValueError:
            continue
        if isinstance(payload, dict):
            return payload
    raise CodexInvocationError("Hermes returned no valid structured result")


__all__ = ["HermesStructuredRunner"]
