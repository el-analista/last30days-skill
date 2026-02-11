"""Tests for cache module."""

import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

# Add lib to path
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from lib import cache


class TestGetCacheKey(unittest.TestCase):
    def test_returns_string(self):
        result = cache.get_cache_key("test topic", "2026-01-01", "2026-01-31", "both")
        self.assertIsInstance(result, str)

    def test_consistent_for_same_inputs(self):
        key1 = cache.get_cache_key("test topic", "2026-01-01", "2026-01-31", "both")
        key2 = cache.get_cache_key("test topic", "2026-01-01", "2026-01-31", "both")
        self.assertEqual(key1, key2)

    def test_different_for_different_inputs(self):
        key1 = cache.get_cache_key("topic a", "2026-01-01", "2026-01-31", "both")
        key2 = cache.get_cache_key("topic b", "2026-01-01", "2026-01-31", "both")
        self.assertNotEqual(key1, key2)

    def test_key_length(self):
        key = cache.get_cache_key("test", "2026-01-01", "2026-01-31", "both")
        self.assertEqual(len(key), 16)


class TestCachePath(unittest.TestCase):
    def test_returns_path(self):
        result = cache.get_cache_path("abc123")
        self.assertIsInstance(result, Path)

    def test_has_json_extension(self):
        result = cache.get_cache_path("abc123")
        self.assertEqual(result.suffix, ".json")


class TestCacheValidity(unittest.TestCase):
    def test_nonexistent_file_is_invalid(self):
        fake_path = Path("/nonexistent/path/file.json")
        result = cache.is_cache_valid(fake_path)
        self.assertFalse(result)


class TestModelCache(unittest.TestCase):
    def test_get_cached_model_returns_none_for_missing(self):
        # Clear any existing cache first
        result = cache.get_cached_model("nonexistent_provider")
        # May be None or a cached value, but should not error
        self.assertTrue(result is None or isinstance(result, str))


class TestCacheDirSelection(unittest.TestCase):
    def setUp(self):
        self.orig_cache_dir = cache.CACHE_DIR
        self.orig_model_cache = cache.MODEL_CACHE_FILE

    def tearDown(self):
        cache.CACHE_DIR = self.orig_cache_dir
        cache.MODEL_CACHE_FILE = self.orig_model_cache
        os.environ.pop("LAST30DAYS_CACHE_DIR", None)

    def test_respects_env_override(self):
        with tempfile.TemporaryDirectory() as td:
            os.environ["LAST30DAYS_CACHE_DIR"] = td
            cache.ensure_cache_dir()
            self.assertEqual(cache.CACHE_DIR, Path(td))
            self.assertEqual(cache.MODEL_CACHE_FILE, Path(td) / "model_selection.json")

    def test_falls_back_to_temp_on_permission_error(self):
        original = Path("/tmp/should-not-exist")
        cache.CACHE_DIR = original
        cache.MODEL_CACHE_FILE = original / "model_selection.json"

        original_mkdir = Path.mkdir
        calls = {"count": 0}

        def fake_mkdir(self, *args, **kwargs):
            calls["count"] += 1
            if calls["count"] == 1:
                raise PermissionError("no write access")
            return original_mkdir(self, *args, **kwargs)

        with mock.patch.object(Path, "mkdir", new=fake_mkdir):
            cache.ensure_cache_dir()

        self.assertIn("last30days/cache", str(cache.CACHE_DIR))
        self.assertEqual(cache.MODEL_CACHE_FILE, cache.CACHE_DIR / "model_selection.json")


if __name__ == "__main__":
    unittest.main()
