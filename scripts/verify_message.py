#!/usr/bin/env python3
"""
Verify agent message signature against agents.yaml registry
Usage: python3 scripts/verify_message.py <message.md> <agent_name>
"""

import sys
import hashlib
import base64
import re
import yaml
from pathlib import Path

def extract_signature(message_content: str) -> tuple:
    """Extract payload, signature, and hash from signed message"""
    
    # Find signature block
    sig_pattern = r'-----BEGIN SSH SIGNATURE-----\n(.*?)\n-----END SSH SIGNATURE-----'
    sig_match = re.search(sig_pattern, message_content, re.DOTALL)
    
    if not sig_match:
        return None, None, None, "No signature block found"
    
    signature_b64 = sig_match.group(1).strip()
    
    # Extract hash
    hash_pattern = r'\*\*Payload Hash \(SHA256\):\*\* ([a-f0-9]{64})'
    hash_match = re.search(hash_pattern, message_content)
    
    if not hash_match:
        return None, None, None, "No hash found in message"
    
    claimed_hash = hash_match.group(1)
    
    # Extract original payload (everything before authentication section)
    auth_section = "### Message Authentication"
    if auth_section in message_content:
        payload = message_content.split(auth_section)[0].rstrip()
    else:
        payload = message_content[:sig_match.start()].rstrip()
    
    return payload, signature_b64, claimed_hash, None

def load_public_key(agent_name: str) -> str:
    """Load public key from agents.yaml"""
    
    agents_yaml = Path('agents/agents.yaml')
    
    if not agents_yaml.exists():
        return None, "agents.yaml not found"
    
    with open(agents_yaml, 'r') as f:
        config = yaml.safe_load(f)
    
    if 'agents' not in config or agent_name not in config['agents']:
        return None, f"Agent '{agent_name}' not found in registry"
    
    agent_config = config['agents'][agent_name]
    
    if 'authentication' not in agent_config:
        return None, f"No authentication config for agent '{agent_name}'"
    
    auth_config = agent_config['authentication']
    
    if auth_config.get('status') == 'pending_generation':
        return None, f"Agent '{agent_name}' key pending generation"
    
    public_key = auth_config.get('public_key')
    
    if not public_key or public_key == 'PENDING_GENERATION':
        return None, f"No public key for agent '{agent_name}'"
    
    return public_key, None

def verify_hash(payload: str, claimed_hash: str) -> bool:
    """Verify SHA256 hash of payload"""
    calculated_hash = hashlib.sha256(payload.encode('utf-8')).hexdigest()
    return calculated_hash == claimed_hash

def verify_signature(payload: str, signature_b64: str, public_key: str) -> tuple:
    """Verify Ed25519 signature (simplified - would use ssh-keygen -Y verify in production)"""
    
    import tempfile
    import subprocess
    import os
    
    # Create temporary files
    with tempfile.NamedTemporaryFile(mode='w', suffix='.pub', delete=False) as f:
        f.write(public_key + '\n')
        pubkey_file = f.name
    
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
        f.write(payload)
        payload_file = f.name
    
    with tempfile.NamedTemporaryFile(mode='wb', delete=False) as f:
        f.write(base64.b64decode(signature_b64))
        sig_file = f.name
    
    try:
        # Verify using ssh-keygen
        result = subprocess.run([
            'ssh-keygen', '-Y', 'verify',
            '-f', pubkey_file,
            '-I', 'agent',
            '-n', 'agent-mesh',
            '-s', sig_file,
            payload_file
        ], capture_output=True, text=True)
        
        is_valid = result.returncode == 0
        error_msg = result.stderr if not is_valid else None
        
    except Exception as e:
        is_valid = False
        error_msg = str(e)
    
    finally:
        # Cleanup
        os.unlink(pubkey_file)
        os.unlink(payload_file)
        os.unlink(sig_file)
    
    return is_valid, error_msg

def verify_message(message_file: str, agent_name: str) -> bool:
    """Full verification workflow"""
    
    print(f"🔍 Verifying: {message_file}")
    print(f"   Agent: {agent_name}")
    
    # Read message
    try:
        with open(message_file, 'r') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"❌ Message file not found: {message_file}")
        return False
    
    # Extract components
    payload, signature_b64, claimed_hash, error = extract_signature(content)
    
    if error:
        print(f"❌ Extraction failed: {error}")
        return False
    
    print(f"   Hash: {claimed_hash[:16]}...")
    
    # Load public key
    public_key, error = load_public_key(agent_name)
    
    if error:
        print(f"❌ Key lookup failed: {error}")
        return False
    
    print(f"   Public key loaded from agents.yaml")
    
    # Verify hash
    if not verify_hash(payload, claimed_hash):
        print(f"❌ Hash verification failed")
        print(f"   Message may have been tampered with")
        return False
    
    print(f"   ✅ Hash verified (SHA256)")
    
    # Verify signature
    is_valid, error = verify_signature(payload, signature_b64, public_key)
    
    if not is_valid:
        print(f"❌ Signature verification failed")
        if error:
            print(f"   Error: {error}")
        return False
    
    print(f"   ✅ Ed25519 signature valid")
    print(f"\n🛡️  Message AUTHENTIC — Sent by {agent_name}")
    
    return True

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 scripts/verify_message.py <message.md> <agent_name>")
        print("Example: python3 scripts/verify_message.py research.md clawdy")
        sys.exit(1)
    
    is_valid = verify_message(sys.argv[1], sys.argv[2])
    sys.exit(0 if is_valid else 1)
