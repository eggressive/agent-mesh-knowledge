#!/usr/bin/env python3
"""
Sign agent message with Ed25519 SSH key
Usage: python3 scripts/sign_message.py <message.md> <agent_name>
"""

import sys
import hashlib
import base64
import subprocess
from pathlib import Path

def sign_message(message_file: str, agent_name: str) -> str:
    """Sign message and append signature block"""
    
    # Read message content
    with open(message_file, 'r') as f:
        content = f.read()
    
    # Calculate SHA256 hash of content
    content_hash = hashlib.sha256(content.encode('utf-8')).hexdigest()
    
    # Load private key
    private_key_path = Path.home() / f'.agent-keys/{agent_name}_key'
    
    if not private_key_path.exists():
        print(f"❌ Private key not found: {private_key_path}")
        print(f"Generate with: ssh-keygen -t ed25519 -f ~/.agent-keys/{agent_name}_key")
        sys.exit(1)
    
    # Create detached signature using ssh-keygen
    sig_file = f"{message_file}.sig"
    
    try:
        subprocess.run([
            'ssh-keygen', '-Y', 'sign',
            '-f', str(private_key_path),
            '-n', 'agent-mesh',
            message_file
        ], check=True, capture_output=True)
        
        # Read signature
        with open(sig_file, 'rb') as f:
            signature_bytes = f.read()
        signature_b64 = base64.b64encode(signature_bytes).decode('ascii')
        
        # Clean up .sig file
        Path(sig_file).unlink()
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Signing failed: {e}")
        sys.exit(1)
    
    # Append signature block to message
    signed_message = content + f"""

---

### Message Authentication
**Agent:** {agent_name}
**Payload Hash (SHA256):** {content_hash}
**Signature Algorithm:** Ed25519 (SSH)
**Namespace:** agent-mesh

### Signature
-----BEGIN SSH SIGNATURE-----
{signature_b64}
-----END SSH SIGNATURE-----

### Verification
```bash
# Verify this message
python3 scripts/verify_message.py {message_file} {agent_name}
```
"""
    
    # Write signed message
    with open(message_file, 'w') as f:
        f.write(signed_message)
    
    print(f"✅ Message signed: {message_file}")
    print(f"   Agent: {agent_name}")
    print(f"   Hash: {content_hash[:16]}...")
    
    return signed_message

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 scripts/sign_message.py <message.md> <agent_name>")
        print("Example: python3 scripts/sign_message.py research.md clawdy")
        sys.exit(1)
    
    sign_message(sys.argv[1], sys.argv[2])
