import json
import unittest
from types import SimpleNamespace
from unittest import mock

from workshop.errors import ContractError
from workshop.runtime.engine import configured_engine, detect_engine, resolve_model
from workshop.runtime.execution import grok_subprocess_environment
from workshop.runtime.grok import GrokStructuredRunner
from workshop.runtime.hermes import HermesStructuredRunner, _decode_json_object


class EngineSelectionTest(unittest.TestCase):
    def test_library_default_stays_codex(self):
        with mock.patch.dict("os.environ", {}, clear=True):
            self.assertEqual(configured_engine(), "codex")

    def test_auto_prefers_ready_grok(self):
        with mock.patch(
            "workshop.runtime.engine.grok_cli_ready", return_value=True
        ), mock.patch(
            "workshop.runtime.engine.hermes_cli_ready", return_value=True
        ):
            self.assertEqual(detect_engine({"WORKSHOP_ENGINE": "auto"}), "grok")

    def test_auto_falls_back_to_hermes_then_codex(self):
        with mock.patch(
            "workshop.runtime.engine.grok_cli_ready", return_value=False
        ), mock.patch(
            "workshop.runtime.engine.hermes_cli_ready", return_value=True
        ):
            self.assertEqual(detect_engine({"WORKSHOP_ENGINE": "auto"}), "hermes")
        with mock.patch(
            "workshop.runtime.engine.grok_cli_ready", return_value=False
        ), mock.patch(
            "workshop.runtime.engine.hermes_cli_ready", return_value=False
        ):
            self.assertEqual(detect_engine({"WORKSHOP_ENGINE": "auto"}), "codex")

    def test_codex_model_names_do_not_leak_into_grok(self):
        self.assertEqual(resolve_model("gpt-5.6-terra", engine="grok"), "grok-4.6")
        self.assertEqual(resolve_model("grok-4.5", engine="grok"), "grok-4.5")


class GrokRunnerTest(unittest.TestCase):
    def test_invoke_reads_structured_output_and_scrubs_factory_env(self):
        observed = {}

        def runner(command, **kwargs):
            observed["command"] = command
            observed["env"] = kwargs["env"]
            return SimpleNamespace(
                returncode=0,
                stdout=json.dumps(
                    {
                        "structuredOutput": {"ok": False},
                        "text": 'note {"ok": true}',
                    }
                ),
                stderr="",
            )

        with mock.patch.dict(
            "os.environ",
            {"HOME": "/tmp/workshop-home", "FACTORY_PASSWORD": "secret", "PATH": "/bin"},
            clear=True,
        ):
            result = GrokStructuredRunner(
                model="grok-4.6",
                reasoning_effort="low",
                binary="/fixture/grok",
                runner=runner,
                cli_version="1.0.5",
            ).invoke(prompt="prove it", schema={"type": "object"})
        self.assertEqual(result, {"ok": True})
        self.assertNotIn("--json-schema", observed["command"])
        self.assertNotIn("--verbatim", observed["command"])
        self.assertIn("--disable-web-search", observed["command"])
        self.assertIn("--max-turns", observed["command"])
        self.assertNotIn("FACTORY_PASSWORD", observed["env"])
        self.assertEqual(observed["env"]["HOME"], "/tmp/workshop-home")

    def test_web_search_turn_keeps_tools_enabled(self):
        observed = {}

        def runner(command, **kwargs):
            observed["command"] = command
            return SimpleNamespace(
                returncode=0,
                stdout=json.dumps(
                    {
                        "structuredOutput": None,
                        "text": 'note {"ok": true}',
                    }
                ),
                stderr="",
            )

        result = GrokStructuredRunner(
            model="grok-4.6",
            reasoning_effort="low",
            binary="/fixture/grok",
            runner=runner,
            cli_version="1.0.5",
        ).invoke(
            prompt="search it",
            schema={"type": "object"},
            native_web_search=True,
        )
        self.assertEqual(result, {"ok": True})
        self.assertNotIn("--json-schema", observed["command"])
        self.assertNotIn("--verbatim", observed["command"])
        self.assertNotIn("--disable-web-search", observed["command"])
        self.assertIn("--always-approve", observed["command"])

    def test_prefers_largest_text_object_and_promotes_json_ints(self):
        payload = GrokStructuredRunner(
            model="grok-4.6",
            reasoning_effort="low",
            binary="/fixture/grok",
            runner=lambda *args, **kwargs: SimpleNamespace(
                returncode=0,
                stdout=json.dumps(
                    {
                        "structuredOutput": {"ok": False},
                        "text": '{"skip": true} note {"ok": true, "axis_direction": [0, 0, 1], "start_deg": 0}',
                    }
                ),
                stderr="",
            ),
            cli_version="1.0.5",
        ).invoke(prompt="prove it", schema={"type": "object"})
        self.assertEqual(payload["ok"], True)
        self.assertEqual(payload["axis_direction"], [0.0, 0.0, 1.0])
        self.assertEqual(payload["start_deg"], 0.0)

    def test_rejects_codex_model_names(self):
        with self.assertRaises(ContractError):
            GrokStructuredRunner(
                model="gpt-5.6-terra",
                reasoning_effort="low",
                binary="/fixture/grok",
                cli_version="1.0.0",
            )


class HermesDecodeTest(unittest.TestCase):
    def test_extracts_json_object_from_noisy_stdout(self):
        payload = _decode_json_object('note\n{"inventor_ids": ["bob"], "rationale": "motion"}\n')
        self.assertEqual(payload["inventor_ids"], ["bob"])

    def test_hermes_runner_does_not_forward_factory_secret(self):
        observed = {}

        def runner(command, **kwargs):
            observed["env"] = kwargs["env"]
            observed["command"] = command
            return SimpleNamespace(returncode=0, stdout='{"ok": true}', stderr="")

        with mock.patch.dict(
            "os.environ",
            {
                "HOME": "/tmp/workshop-home",
                "HERMES_HOME": "/tmp/hermes-home",
                "FACTORY_PASSWORD": "secret",
                "PATH": "/bin",
            },
            clear=True,
        ):
            result = HermesStructuredRunner(
                model="grok-4.6",
                reasoning_effort="low",
                binary="/fixture/hermes",
                runner=runner,
                cli_version="0.20.5",
            ).invoke(prompt="prove it", schema={"type": "object"})
        self.assertEqual(result, {"ok": True})
        self.assertNotIn("FACTORY_PASSWORD", observed["env"])
        self.assertEqual(observed["env"]["HERMES_HOME"], "/tmp/hermes-home")


class GrokEnvironmentTest(unittest.TestCase):
    def test_grok_env_allowlist(self):
        env = grok_subprocess_environment(
            {
                "HOME": "/home/marc",
                "PATH": "/bin",
                "FACTORY_PASSWORD": "nope",
                "OPENAI_API_KEY": "nope",
            }
        )
        self.assertEqual(env["HOME"], "/home/marc")
        self.assertNotIn("FACTORY_PASSWORD", env)
        self.assertNotIn("OPENAI_API_KEY", env)


if __name__ == "__main__":
    unittest.main()
