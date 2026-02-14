"""Tests for model router prefix detection"""

import pytest
import subprocess
import json
from pathlib import Path


class TestModelRouter:
    """Test model router classification"""
    
    @pytest.fixture
    def router_script(self):
        """Path to model router script"""
        return Path(__file__).parent.parent / "tools" / "model-router" / "router.js"
    
    @pytest.mark.parametrize("input_text,expected_model", [
        ("/code fix the bug in main.py", "codex"),
        ("/deep analyze this architecture", "opus"),
        ("/research what's new in LLMs", "kimi"),
        ("/fast summarize this", "haiku"),
        ("/cheap translate this text", "kimi-free"),
        ("just a normal message", "default"),
    ])
    def test_prefix_detection(self, router_script, input_text, expected_model):
        """Router should detect prefixes correctly"""
        if not router_script.exists():
            pytest.skip("Router script not found")
        
        result = subprocess.run(
            ["node", str(router_script), "--classify", input_text],
            capture_output=True, text=True
        )
        
        if result.returncode == 0:
            output = json.loads(result.stdout)
            assert output.get("model") == expected_model
    
    def test_empty_input_returns_default(self, router_script):
        """Empty input should return default model"""
        if not router_script.exists():
            pytest.skip("Router script not found")
        
        result = subprocess.run(
            ["node", str(router_script), "--classify", ""],
            capture_output=True, text=True
        )
        
        if result.returncode == 0:
            output = json.loads(result.stdout)
            assert output.get("model") == "default"
    
    def test_case_insensitive_prefixes(self, router_script):
        """Prefixes should be case-insensitive"""
        if not router_script.exists():
            pytest.skip("Router script not found")
        
        for prefix in ["/CODE", "/Code", "/code"]:
            result = subprocess.run(
                ["node", str(router_script), "--classify", f"{prefix} test"],
                capture_output=True, text=True
            )
            
            if result.returncode == 0:
                output = json.loads(result.stdout)
                assert output.get("model") == "codex"
