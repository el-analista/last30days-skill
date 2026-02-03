"""Bird CLI client for X (Twitter) search."""

import json
import shutil
import subprocess
import sys
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple


def _log(msg: str):
    """Log to stderr."""
    sys.stderr.write(f"[Bird] {msg}\n")
    sys.stderr.flush()


def is_bird_installed() -> bool:
    """Check if Bird CLI is installed.

    Returns:
        True if 'bird' command is available in PATH, False otherwise.
    """
    return shutil.which("bird") is not None


def is_bird_authenticated() -> Optional[str]:
    """Check if Bird is authenticated by running 'bird whoami'.

    Returns:
        Username if authenticated, None otherwise.
    """
    if not is_bird_installed():
        return None

    try:
        result = subprocess.run(
            ["bird", "whoami"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        if result.returncode == 0 and result.stdout.strip():
            # Output is typically the username
            return result.stdout.strip().split('\n')[0]
        return None
    except (subprocess.TimeoutExpired, FileNotFoundError, subprocess.SubprocessError):
        return None


def check_npm_available() -> bool:
    """Check if npm is available for installation.

    Returns:
        True if 'npm' command is available in PATH, False otherwise.
    """
    return shutil.which("npm") is not None


def install_bird() -> Tuple[bool, str]:
    """Install Bird CLI via npm.

    Returns:
        Tuple of (success, message).
    """
    if not check_npm_available():
        return False, "npm not found. Install Node.js first, or install Bird manually: https://github.com/steipete/bird"

    try:
        _log("Installing Bird CLI...")
        result = subprocess.run(
            ["npm", "install", "-g", "@steipete/bird"],
            capture_output=True,
            text=True,
            timeout=120,
        )
        if result.returncode == 0:
            return True, "Bird CLI installed successfully!"
        else:
            error = result.stderr.strip() or result.stdout.strip() or "Unknown error"
            return False, f"Installation failed: {error}"
    except subprocess.TimeoutExpired:
        return False, "Installation timed out"
    except Exception as e:
        return False, f"Installation error: {e}"


def get_bird_status() -> Dict[str, Any]:
    """Get comprehensive Bird status.

    Returns:
        Dict with keys: installed, authenticated, username, can_install
    """
    installed = is_bird_installed()
    username = is_bird_authenticated() if installed else None

    return {
        "installed": installed,
        "authenticated": username is not None,
        "username": username,
        "can_install": check_npm_available(),
    }