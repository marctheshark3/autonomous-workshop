"""Select the native coding-agent CLI behind Workshop structured calls.

Codex remains the default library engine so existing tests and upstream
behavior stay pinned. `workshop wish` may set WORKSHOP_ENGINE=auto, which
prefers an authenticated Grok CLI, then Hermes, then Codex.
"""

from __future__ import annotations

import os
import shutil
import subprocess
from typing import Any, Mapping, Optional

from workshop.errors import ContractError
from workshop.runtime.codex import CodexStructuredRunner
from workshop.runtime.execution import (
    codex_subprocess_environment,
    grok_subprocess_environment,
    hermes_subprocess_environment,
)


ENGINES = frozenset(("auto", "codex", "grok", "hermes"))
ALLOWED_GROK_MODELS = frozenset(("grok-4.6", "grok-4.5"))
DEFAULT_GROK_MODEL = "grok-4.6"
DEFAULT_HERMES_MODEL = "grok-4.6"
DEFAULT_HERMES_PROVIDER = "xai-oauth"


def configured_engine(source: Optional[Mapping[str, str]] = None) -> str:
    values = os.environ if source is None else source
    requested = (values.get("WORKSHOP_ENGINE") or "codex").strip().lower()
    if requested not in ENGINES:
        raise ContractError("WORKSHOP_ENGINE must be auto, codex, grok, or hermes")
    if requested == "auto":
        return detect_engine(values)
    return requested


def detect_engine(source: Optional[Mapping[str, str]] = None) -> str:
    values = os.environ if source is None else source
    requested = (values.get("WORKSHOP_ENGINE") or "auto").strip().lower()
    if requested in ("codex", "grok", "hermes"):
        return requested
    if requested not in ("auto", ""):
        raise ContractError("WORKSHOP_ENGINE must be auto, codex, grok, or hermes")
    if grok_cli_ready(values):
        return "grok"
    if hermes_cli_ready(values):
        return "hermes"
    return "codex"


def grok_binary(source: Optional[Mapping[str, str]] = None) -> Optional[str]:
    values = os.environ if source is None else source
    return values.get("WORKSHOP_GROK_BIN") or shutil.which("grok")


def hermes_binary(source: Optional[Mapping[str, str]] = None) -> Optional[str]:
    values = os.environ if source is None else source
    return values.get("WORKSHOP_HERMES_BIN") or shutil.which("hermes")


def grok_cli_ready(source: Optional[Mapping[str, str]] = None) -> bool:
    binary = grok_binary(source)
    if not binary:
        return False
    try:
        completed = subprocess.run(
            [binary, "models"],
            capture_output=True,
            text=True,
            timeout=15,
            check=False,
            env=dict(grok_subprocess_environment(source)),
        )
    except (OSError, subprocess.SubprocessError):
        return False
    output = "%s\n%s" % (completed.stdout or "", completed.stderr or "")
    return completed.returncode == 0 and "logged in" in output.lower()


def hermes_cli_ready(source: Optional[Mapping[str, str]] = None) -> bool:
    binary = hermes_binary(source)
    if not binary:
        return False
    try:
        completed = subprocess.run(
            [binary, "--version"],
            capture_output=True,
            text=True,
            timeout=15,
            check=False,
            env=dict(hermes_subprocess_environment(source)),
        )
    except (OSError, subprocess.SubprocessError):
        return False
    return completed.returncode == 0 and bool((completed.stdout or "").strip())


def resolve_model(requested: Optional[str], *, engine: str) -> str:
    if engine == "grok":
        if requested in ALLOWED_GROK_MODELS:
            return requested
        configured = os.environ.get("WORKSHOP_GROK_MODEL")
        if configured in ALLOWED_GROK_MODELS:
            return configured
        return DEFAULT_GROK_MODEL
    if engine == "hermes":
        if requested and requested not in ("gpt-5.6-terra", "gpt-5.6-luna"):
            return requested
        return os.environ.get("WORKSHOP_HERMES_MODEL") or DEFAULT_HERMES_MODEL
    if not requested:
        raise ContractError("Codex structured runner requires an explicit model")
    return requested


def structured_runner(
    *,
    reasoning_effort: str,
    model: Optional[str] = None,
    default_codex_model: Optional[str] = None,
    binary: Optional[str] = None,
    timeout_seconds: Optional[int] = None,
    runner: Any = subprocess.run,
) -> Any:
    engine = configured_engine()
    if engine == "grok":
        from workshop.runtime.grok import GrokStructuredRunner

        kwargs = {
            "model": resolve_model(model, engine="grok"),
            "reasoning_effort": reasoning_effort,
            "binary": binary,
            "runner": runner,
        }
        if timeout_seconds is not None:
            kwargs["timeout_seconds"] = timeout_seconds
        return GrokStructuredRunner(**kwargs)
    if engine == "hermes":
        from workshop.runtime.hermes import HermesStructuredRunner

        kwargs = {
            "model": resolve_model(model, engine="hermes"),
            "reasoning_effort": reasoning_effort,
            "binary": binary,
            "runner": runner,
        }
        if timeout_seconds is not None:
            kwargs["timeout_seconds"] = timeout_seconds
        return HermesStructuredRunner(**kwargs)
    kwargs = {
        "model": model or default_codex_model,
        "reasoning_effort": reasoning_effort,
        "binary": binary,
        "runner": runner,
    }
    if timeout_seconds is not None:
        kwargs["timeout_seconds"] = timeout_seconds
    return CodexStructuredRunner(**kwargs)


def worker_runtime_environment(
    source: Optional[Mapping[str, str]] = None,
) -> Mapping[str, str]:
    values = os.environ if source is None else source
    engine = configured_engine(values)
    environment = dict(codex_subprocess_environment(values))
    if engine == "grok":
        environment.update(grok_subprocess_environment(values))
    elif engine == "hermes":
        environment.update(hermes_subprocess_environment(values))
    return environment


__all__ = [
    "ALLOWED_GROK_MODELS",
    "DEFAULT_GROK_MODEL",
    "DEFAULT_HERMES_MODEL",
    "DEFAULT_HERMES_PROVIDER",
    "ENGINES",
    "configured_engine",
    "detect_engine",
    "grok_binary",
    "grok_cli_ready",
    "hermes_binary",
    "hermes_cli_ready",
    "resolve_model",
    "structured_runner",
    "worker_runtime_environment",
]
