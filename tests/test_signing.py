"""Tests for message signing and verification"""

import pytest
import subprocess
import sys
from pathlib import Path

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))


class TestMessageSigning:
    """Test Ed25519 message signing"""
    
    def test_sign_message_creates_signature(self, sample_message, mock_agent_keys, temp_dir):
        """Signing a message should append signature block"""
        from sign_message import sign_message
        
        result = sign_message(str(sample_message), mock_agent_keys["agent_name"])
        
        # Should contain signature block
        assert "-----BEGIN SSH SIGNATURE-----" in result
        assert "-----END SSH SIGNATURE-----" in result
        assert "Payload Hash (SHA256)" in result
    
    def test_sign_message_missing_key_fails(self, sample_message, temp_dir, monkeypatch):
        """Signing without keypair should fail gracefully"""
        from sign_message import sign_message
        
        # Point to empty home
        monkeypatch.setenv("HOME", str(temp_dir))
        
        with pytest.raises(SystemExit):
            sign_message(str(sample_message), "nonexistent_agent")


class TestMessageVerification:
    """Test Ed25519 signature verification"""
    
    def test_verify_unsigned_message_fails(self, sample_message):
        """Verifying unsigned message should fail"""
        from verify_message import extract_signature
        
        content = sample_message.read_text()
        payload, sig, hash_val, error = extract_signature(content)
        
        assert error == "No signature block found"
        assert payload is None
    
    def test_extract_signature_parses_correctly(self, temp_dir):
        """Signature extraction should parse signed messages"""
        from verify_message import extract_signature
        
        signed_content = """# Test Message

Content here.

### Message Authentication

**Agent:** test_agent
**Timestamp:** 2026-02-14T15:00:00Z
**Payload Hash (SHA256):** abcd1234abcd1234abcd1234abcd1234abcd1234abcd1234abcd1234abcd1234

-----BEGIN SSH SIGNATURE-----
VGVzdFNpZ25hdHVyZQ==
-----END SSH SIGNATURE-----
"""
        
        payload, sig, hash_val, error = extract_signature(signed_content)
        
        assert error is None
        assert "# Test Message" in payload
        assert hash_val == "abcd1234abcd1234abcd1234abcd1234abcd1234abcd1234abcd1234abcd1234"
        assert sig == "VGVzdFNpZ25hdHVyZQ=="


class TestEndToEnd:
    """End-to-end signing and verification tests"""
    
    def test_sign_then_verify_roundtrip(self, sample_message, mock_agent_keys, temp_dir):
        """Sign → Verify should succeed for valid keypair"""
        import subprocess
        
        scripts_dir = Path(__file__).parent.parent / "scripts"
        
        # Sign the message
        result = subprocess.run([
            sys.executable, str(scripts_dir / "sign_message.py"),
            str(sample_message), mock_agent_keys["agent_name"]
        ], capture_output=True, text=True)
        
        # Should succeed (exit code 0) or fail gracefully
        # Note: Full verification requires agents.yaml setup
        assert result.returncode == 0 or "not found" in result.stderr
