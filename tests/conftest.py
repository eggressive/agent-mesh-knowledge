"""Pytest configuration and shared fixtures"""

import pytest
import tempfile
import os
from pathlib import Path


@pytest.fixture
def temp_dir():
    """Create a temporary directory for test files"""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def sample_message(temp_dir):
    """Create a sample message file for testing"""
    msg_file = temp_dir / "test_message.md"
    msg_file.write_text("""# Test Message

This is a test message for the Multi-Agent Knowledge Mesh.

## Content

- Item 1
- Item 2
- Item 3

**Timestamp:** 2026-02-14T15:00:00Z
""")
    return msg_file


@pytest.fixture
def mock_agent_keys(temp_dir, monkeypatch):
    """Create mock Ed25519 keypair for testing"""
    import subprocess
    
    keys_dir = temp_dir / ".agent-keys"
    keys_dir.mkdir()
    
    # Generate test keypair
    key_path = keys_dir / "test_agent_key"
    subprocess.run([
        "ssh-keygen", "-t", "ed25519",
        "-f", str(key_path),
        "-N", "",  # No passphrase
        "-q"
    ], check=True)
    
    # Monkeypatch home directory
    monkeypatch.setenv("HOME", str(temp_dir))
    
    return {
        "private_key": key_path,
        "public_key": Path(str(key_path) + ".pub"),
        "agent_name": "test_agent"
    }
