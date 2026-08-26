"""Bounded structured-output calls through an installed authenticated Grok CLI."""

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import tempfile
import time
from pathlib import Path
from typing import Any, Mapping, Optional

from workshop.errors import ContractError
from workshop.runtime.codex import (
    DEFAULT_CODEX_TIMEOUT_SECONDS,
    MAX_CODEX_OUTPUT_BYTES,
    CodexInvocationError,
)
from workshop.runtime.engine import ALLOWED_GROK_MODELS
from workshop.runtime.execution import grok_subprocess_environment


class GrokStructuredRunner:
    def __init__(
        self,
        *,
        model: str,
        reasoning_effort: str,
        binary: Optional[str] = None,
        timeout_seconds: int = DEFAULT_CODEX_TIMEOUT_SECONDS,
        runner: Any = subprocess.run,
        cli_version: Optional[str] = None,
    ) -> None:
        if model not in ALLOWED_GROK_MODELS:
            raise ContractError("Workshop Grok model must be grok-4.6 or grok-4.5")
        if reasoning_effort not in ("low", "medium", "high", "xhigh"):
            raise ValueError("unsupported Grok reasoning effort")
        if type(timeout_seconds) is not int or not 1 <= timeout_seconds <= 3_600:
            raise ValueError("Grok timeout_seconds must be from 1 to 3,600")
        self.binary = binary or os.environ.get("WORKSHOP_GROK_BIN") or shutil.which("grok")
        self.model = model
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
                env=grok_subprocess_environment(),
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
            raise CodexInvocationError("Grok CLI is not installed or on PATH")
        if type(native_web_search) is not bool:
            raise ValueError("native_web_search must be a boolean")

        self.last_used_web_search = False
        deadline = time.monotonic() + self.timeout_seconds
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            raise CodexInvocationError("Grok structured call timed out")
        try:
            completed = self._run_attempt(
                prompt=prompt,
                schema=schema,
                workspace=workspace,
                native_web_search=native_web_search,
                timeout_seconds=remaining,
            )
        except subprocess.TimeoutExpired as exc:
            exc.output = None
            exc.stderr = None
            raise CodexInvocationError("Grok structured call timed out") from None
        except (OSError, subprocess.SubprocessError, TypeError, ValueError):
            raise CodexInvocationError(
                "Grok could not execute the structured call"
            ) from None

        stdout = completed.stdout if isinstance(completed.stdout, str) else ""
        if completed.returncode != 0:
            raise CodexInvocationError("Grok did not complete the structured call")
        payload = _decode_grok_payload(stdout.encode("utf-8"))
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
        with tempfile.TemporaryDirectory(prefix="workshop-grok-") as temporary:
            control_root = Path(temporary)
            prompt_path = control_root / "prompt.txt"
            if native_web_search:
                written = (
                    prompt
                    + "\nReturn only JSON matching this schema.\nSCHEMA:\n"
                    + json.dumps(schema, sort_keys=True)
                )
            else:
                written = prompt
            prompt_path.write_text(written, encoding="utf-8")
            cwd = Path(workspace).resolve() if workspace is not None else control_root
            cwd.mkdir(parents=True, exist_ok=True)
            command = [
                self.binary,
                "--prompt-file",
                str(prompt_path),
                "--output-format",
                "json",
                "--cwd",
                str(cwd),
                "--no-plan",
                "--no-subagents",
                "--reasoning-effort",
                self.reasoning_effort,
                "-m",
                self.model,
            ]
            if native_web_search:
                command.extend(("--always-approve", "--max-turns", "8"))
            else:
                command.extend(
                    (
                        "--json-schema",
                        json.dumps(schema, sort_keys=True, separators=(",", ":")),
                        "--permission-mode",
                        "dontAsk",
                        "--verbatim",
                        "--disable-web-search",
                        "--max-turns",
                        "1",
                    )
                )
            return self._runner(
                command,
                capture_output=True,
                text=True,
                timeout=timeout_seconds,
                check=False,
                env=grok_subprocess_environment(),
            )


def _first_json_object(text: str) -> Mapping[str, Any]:
    start = text.find("{")
    if start < 0:
        raise ValueError("no object")
    payload, _end = json.JSONDecoder().raw_decode(text[start:])
    if not isinstance(payload, dict):
        raise ValueError("not an object")
    return payload


def _decode_grok_payload(encoded: bytes) -> Mapping[str, Any]:
    if not encoded:
        raise CodexInvocationError("Grok returned no structured result")
    if len(encoded) > MAX_CODEX_OUTPUT_BYTES:
        raise CodexInvocationError("Grok structured result exceeded the safe size limit")
    try:
        envelope = json.loads(encoded.decode("utf-8"))
    except (UnicodeError, ValueError):
        raise CodexInvocationError("Grok returned no valid structured result") from None
    if isinstance(envelope, dict) and isinstance(envelope.get("structuredOutput"), dict):
        return envelope["structuredOutput"]
    if isinstance(envelope, dict) and isinstance(envelope.get("text"), str):
        try:
            return _first_json_object(envelope["text"])
        except ValueError:
            raise CodexInvocationError("Grok returned no valid structured result") from None
    if isinstance(envelope, dict) and envelope.get("structuredOutput") is None:
        raise CodexInvocationError("Grok returned no valid structured result")
    if not isinstance(envelope, dict):
        raise CodexInvocationError("Grok structured result must be an object")
    return envelope


__all__ = ["GrokStructuredRunner"]
