"""Explicit subprocess environments for Workshop-owned execution boundaries.

CAD and slicer programs never need account credentials, so they receive a
small deterministic environment built from constants.  Codex needs access to
its own login state, but not to Factory publishing credentials or arbitrary
secrets inherited by the Workshop process.
"""

from __future__ import annotations

import os
from typing import Mapping, Optional


_CODEX_ENVIRONMENT_NAMES = frozenset(
    (
        # Locate an installed CLI (including an ``env node`` shebang) and its
        # local authenticated state.
        "PATH",
        "HOME",
        "CODEX_HOME",
        "XDG_CONFIG_HOME",
        "XDG_CACHE_HOME",
        # Supported non-interactive Codex authentication inputs.
        "OPENAI_API_KEY",
        "CODEX_API_KEY",
        "OPENAI_ORGANIZATION",
        "OPENAI_PROJECT",
        # Stable process/runtime behavior; none of these carries Workshop or
        # Factory account authority.
        "LANG",
        "LC_ALL",
        "LC_CTYPE",
        "TERM",
        "TMPDIR",
        "SSL_CERT_FILE",
        "SSL_CERT_DIR",
    )
)
_GROK_ENVIRONMENT_NAMES = frozenset(
    (
        "PATH",
        "HOME",
        "GROK_HOME",
        "GROK_SANDBOX",
        "XDG_CONFIG_HOME",
        "XDG_CACHE_HOME",
        "LANG",
        "LC_ALL",
        "LC_CTYPE",
        "TERM",
        "TMPDIR",
        "SSL_CERT_FILE",
        "SSL_CERT_DIR",
    )
)
_HERMES_ENVIRONMENT_NAMES = frozenset(
    (
        "PATH",
        "HOME",
        "HERMES_HOME",
        "HERMES_PROFILE",
        "XDG_CONFIG_HOME",
        "XDG_CACHE_HOME",
        "LANG",
        "LC_ALL",
        "LC_CTYPE",
        "TERM",
        "TMPDIR",
        "SSL_CERT_FILE",
        "SSL_CERT_DIR",
    )
)


def minimal_tool_environment() -> Mapping[str, str]:
    """Return a deterministic, credential-free CAD/slicer environment."""

    return {
        "PATH": os.defpath,
        "LANG": "C",
        "LC_ALL": "C",
        "PYTHONHASHSEED": "0",
        "PYTHONDONTWRITEBYTECODE": "1",
    }


def codex_subprocess_environment(
    source: Optional[Mapping[str, str]] = None,
) -> Mapping[str, str]:
    """Keep only Codex login/runtime inputs from the parent environment.

    The allowlist deliberately excludes every ``FACTORY_*`` and
    ``WORKSHOP_SHOP_*`` value as well as unrelated cloud, Git, package-manager,
    and shell credentials.  This same function is used for version probes and
    model calls so discovery cannot become a credential exfiltration path.
    """

    values = os.environ if source is None else source
    return _allowlisted_environment(values, _CODEX_ENVIRONMENT_NAMES)


def grok_subprocess_environment(
    source: Optional[Mapping[str, str]] = None,
) -> Mapping[str, str]:
    """Keep Grok CLI login/runtime inputs; never Factory credentials."""

    values = os.environ if source is None else source
    return _allowlisted_environment(values, _GROK_ENVIRONMENT_NAMES)


def hermes_subprocess_environment(
    source: Optional[Mapping[str, str]] = None,
) -> Mapping[str, str]:
    """Keep Hermes runtime inputs; credentials stay in Hermes home, not env copy."""

    values = os.environ if source is None else source
    return _allowlisted_environment(values, _HERMES_ENVIRONMENT_NAMES)


def _allowlisted_environment(
    values: Mapping[str, str], names: frozenset[str]
) -> Mapping[str, str]:
    return {
        name: value
        for name in names
        if isinstance((value := values.get(name)), str) and value
    }


__all__ = [
    "codex_subprocess_environment",
    "grok_subprocess_environment",
    "hermes_subprocess_environment",
    "minimal_tool_environment",
]
