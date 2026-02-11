"""Tests for bird_x module."""

import sys
import unittest
from pathlib import Path
from unittest import mock

# Add lib to path
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from lib import bird_x


class TestBirdSearchRetries(unittest.TestCase):
    def test_uses_strongest_token_on_last_chance_retry(self):
        with mock.patch.object(bird_x, "_extract_core_subject", return_value="best codex skill plugin"), \
             mock.patch.object(bird_x, "_run_bird_search", side_effect=[{"items": []}, {"items": []}, {"items": []}]) as run_mock:
            bird_x.search_x("best codex skill plugin", "2026-01-01", "2026-01-31", depth="quick")

        self.assertEqual(run_mock.call_count, 3)
        first_query = run_mock.call_args_list[0].args[0]
        second_query = run_mock.call_args_list[1].args[0]
        third_query = run_mock.call_args_list[2].args[0]

        self.assertEqual(first_query, "best codex skill plugin since:2026-01-01")
        self.assertEqual(second_query, "best codex since:2026-01-01")
        self.assertEqual(third_query, "codex since:2026-01-01")


if __name__ == "__main__":
    unittest.main()
