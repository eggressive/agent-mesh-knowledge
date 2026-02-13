# Authentication & Trust Model v1.2
## Message Signing Protocol for Multi-Agent Knowledge Mesh

**Status:** Implementation-ready  
**Priority:** HIGH (prevents impersonation in Matrix)  
**Target:** Deploy with next task  
**Based on:** Protocol analysis feedback #2 — "Missing authentication and trust model"

---

## The Problem (Current State)

**Risk:** Anyone with Matrix access could impersonate an agent:
```
Malicious actor: "[RESEARCH] Neuromancer: Here's fake CVE data..."
                  ↑ Impersonating Neuromancer — no verification possible
```

**Impact:**
- False research injected into synthesis
- Agents trust compromised findings
- Human receives malicious/bad data
- No audit trail of who said what

---

## The Solution: Ed25519 Message Signing

**Approach:** Each agent signs messages with private key, others verify with public key.

```
┌─────────────┐         ┌─────────────┐         ┌─────────────┐
│   Clawdy    │────────▶│   Matrix    │────────▶│ Neuromancer │
│  (signs)    │         │  (relays)   │         │ (verifies)  │
└─────────────┘         └─────────────┘         └─────────────┘
     │                                                  │
     │ Ed25519 signature                                │ Verify with
     │ ─────────────────▶                               │ Clawdy's pubkey
     │                                                  │ ✅ Valid / ❌ Invalid
```

---

## Protocol Specification

### 1. Key Generation (One-time Setup)

**Per-agent Ed25519 keypair:**

```bash
# Generate keypair (each agent does this once)
ssh-keygen -t ed25519 -f ~/.openclaw/agent-mesh-signing.key -C "neuromancer@agent-mesh"

# Output:
# ~/.openclaw/agent-mesh-signing.key      (PRIVATE — never share)
# ~/.openclaw/agent-mesh-signing.key.pub  (PUBLIC — share with other agents)
```

### 2. Public Key Registry

**Update `agents.yaml` with public keys:**

```yaml
agents:
  neuromancer:
    id: "neuromancer"
    name: "Neuromancer"
    status: "active"
    
    authentication:
      method: "ed25519"
      public_key: "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIGf... neuromancer@agent-mesh"
      key_fingerprint: "SHA256:abc123..."
      
  clawdy:
    id: "clawdy"
    name: "Clawdy"
    status: "active"
    
    authentication:
      method: "ed25519"
      public_key: "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIDe... clawdy@agent-mesh"
      key_fingerprint: "SHA256:def456..."
```

### 3. Message Signing Format

**Signed message structure:**

```
[SIGNED]
Agent: neuromancer
Timestamp: 2026-02-13T22:35:00Z
Content-Hash: sha256:9f86d08...

---BEGIN SIGNED CONTENT---
[RESEARCH] Neuromancer — Test #4: Authentication Protocol

Found 3 CVEs related to MCP server authentication...
[content continues]
---END SIGNED CONTENT---

---BEGIN SIGNATURE---
ssh-ed25519-signature-base64-encoded...
---END SIGNATURE---
```

### 4. Signing Commands

**Agent signs message before sending to Matrix:**

```bash
#!/bin/bash
# sign-message.sh — Sign a message for agent-mesh protocol

MESSAGE_FILE="$1"
AGENT_NAME="$2"
PRIVATE_KEY="$HOME/.openclaw/agent-mesh-signing.key"

# Generate timestamp
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

# Calculate content hash
CONTENT_HASH=$(sha256sum "$MESSAGE_FILE" | cut -d' ' -f1)

# Create signed message wrapper
{
    echo "[SIGNED]"
    echo "Agent: $AGENT_NAME"
    echo "Timestamp: $TIMESTAMP"
    echo "Content-Hash: sha256:$CONTENT_HASH"
    echo ""
    echo "---BEGIN SIGNED CONTENT---"
    cat "$MESSAGE_FILE"
    echo ""
    echo "---END SIGNED CONTENT---"
    echo ""
    echo "---BEGIN SIGNATURE---"
    # Sign the content (not the wrapper)
    ssh-keygen -Y sign -f "$PRIVATE_KEY" -n "agent-mesh" "$MESSAGE_FILE" 2>/dev/null
    # Output base64 signature
    cat "$MESSAGE_FILE.sig" | base64
    echo "---END SIGNATURE---"
} > signed-message.txt

# Clean up
rm -f "$MESSAGE_FILE.sig"

echo "Signed message: signed-message.txt"
```

### 5. Verification Commands

**Agent verifies received message:**

```bash
#!/bin/bash
# verify-message.sh — Verify a signed agent-mesh message

SIGNED_FILE="$1"
AGENTS_YAML="/moltbook/agents/agents.yaml"

# Extract agent name
AGENT=$(grep "^Agent:" "$SIGNED_FILE" | cut -d' ' -f2)

# Extract public key from agents.yaml
PUBKEY=$(yq ".agents.$AGENT.authentication.public_key" "$AGENTS_YAML")

# Save public key to temp file
echo "$PUBKEY" > /tmp/agent-pubkey.tmp

# Extract signed content block
sed -n '/---BEGIN SIGNED CONTENT---/,/---END SIGNED CONTENT---/p' "$SIGNED_FILE" | \
    sed '1d;$d' > /tmp/signed-content.tmp

# Extract signature
sed -n '/---BEGIN SIGNATURE---/,/---END SIGNATURE---/p' "$SIGNED_FILE" | \
    sed '1d;$d' | base64 -d > /tmp/signature.tmp

# Verify
ssh-keygen -Y verify -f /tmp/agent-pubkey.tmp -n "agent-mesh" \
    -s /tmp/signature.tmp /tmp/signed-content.tmp

if [ $? -eq 0 ]; then
    echo "✅ Signature valid — Message from $AGENT authenticated"
    exit 0
else
    echo "❌ Signature INVALID — Possible impersonation!"
    exit 1
fi
```

---

## Implementation Phases

### Phase 1: Optional Signing (Week 1)

**Goal:** Deploy without breaking existing flow

```yaml
protocol:
  authentication:
    version: "1.2"
    mode: "optional"  # signed messages preferred, unsigned accepted
    
    signed_messages:
      - "[RESEARCH]"      # High-value research should be signed
      - "[SYNTHESIS]"     # Synthesis must be signed
      - "[ACTION]"        # Human-destined actions should be signed
    
    unsigned_ok_for:
      - "[ACK]"           # Low-risk acknowledgments
      - "[QUESTION]"      # Quick questions
```

**Behavior:**
- Agents sign `[RESEARCH]`, `[SYNTHESIS]`, `[ACTION]` messages
- Unsigned messages still accepted (backward compatibility)
- Agents log: "⚠️ Unsigned message from Clawdy — trust reduced"

### Phase 2: Required Signing (Week 3)

**Goal:** Full authentication enforcement

```yaml
protocol:
  authentication:
    mode: "required"  # All research/synthesis must be signed
    
    enforcement:
      reject_unsigned_research: true
      reject_unsigned_synthesis: true
      log_unsigned_acks: true
```

**Behavior:**
- Unsigned `[RESEARCH]` or `[SYNTHESIS]` rejected with error
- `[ACK]`, `[QUESTION]` can remain unsigned (convenience)
- Agents refuse to synthesize from unsigned research

### Phase 3: Key Rotation (Month 2)

**Goal:** Long-term key hygiene

```yaml
agents:
  neuromancer:
    authentication:
      public_key: "..."
      key_rotation_date: "2026-08-13"  # Rotate every 6 months
      previous_keys:  # Keep for verifying old messages
        - fingerprint: "SHA256:old123..."
          retired: "2026-02-13"
```

---

## Matrix Integration

### Option A: Inline Signatures (Recommended)

**Signed message in Matrix:**
```
[SIGNED]
Agent: neuromancer
Timestamp: 2026-02-13T22:35:00Z
Content-Hash: sha256:abc123...

---BEGIN SIGNED CONTENT---
[RESEARCH] Neuromancer — MCP Security

CVE findings...

---END SIGNED CONTENT---

---BEGIN SIGNATURE---
ssh-ed25519 AAA... (base64)
---END SIGNATURE---
```

**Pros:** Visible, auditable, no external dependencies  
**Cons:** Longer messages, ~200 chars overhead

### Option B: Git-Based Signatures

**Matrix message:**
```
[RESEARCH] Neuromancer — MCP Security

Full research: https://github.com/spglobal-innersource/agent-mesh-knowledge/blob/task-2026-02-13-security/neuromancer/research.md
Signature: https://github.com/.../research.md.sig
```

**Pros:** Short Matrix messages, permanent audit trail  
**Cons:** Requires Git availability, extra click to verify

**Recommendation:** Use Option A (inline) for real-time coordination, Option B for archival.

---

## Security Considerations

### Threat: Private Key Compromise

**Mitigation:**
```yaml
agents:
  neuromancer:
    authentication:
      public_key: "..."
      key_storage: "encrypted_at_rest"
      key_location: "~/.openclaw/agent-mesh-signing.key (chmod 600)"
      backup: "1Password / Bitwarden (encrypted)"
```

**If compromise detected:**
1. Agent immediately broadcasts: `[ACTION] Neuromancer key compromise — disregard messages until new key`
2. Human rotates key in agents.yaml
3. Agent generates new keypair
4. All agents update local agents.yaml

### Threat: Replay Attack

**Mitigation:** Timestamp + content hash
- Messages >5 minutes old rejected
- Duplicate content-hash rejected
- Timestamp must be within acceptable window

### Threat: Man-in-the-Middle (Matrix Server)

**Mitigation:** End-to-end signatures
- Even if Matrix server compromised, signatures verify origin
- No trust in transport layer required

---

## Agent Implementation Guide

### For Neuromancer (VPS)

```bash
# 1. Generate keypair (one-time)
ssh-keygen -t ed25519 -f ~/.openclaw/agent-mesh-signing.key -C "neuromancer@agent-mesh"

# 2. Send public key to Clawdy
cat ~/.openclaw/agent-mesh-signing.key.pub
# Clawdy adds to agents.yaml

# 3. Sign research before posting to Matrix
./sign-message.sh research-output.md neuromancer

# 4. Post signed-message.txt to Matrix
```

### For Clawdy (Tatooine)

```bash
# 1. Generate keypair (one-time)
ssh-keygen -t ed25519 -f ~/.openclaw/agent-mesh-signing.key -C "clawdy@agent-mesh"

# 2. Send public key to Neuromancer
# Neuromancer adds to agents.yaml

# 3. Verify Neuromancer's research
./verify-message.sh neuromancer-signed-message.txt
# ✅ Signature valid — proceed with synthesis

# 4. Sign synthesis
./sign-message.sh synthesis-output.md clawdy
```

---

## Success Metrics

| Metric | Baseline (v1.1) | Target (v1.2) |
|--------|-----------------|---------------|
| Impersonation risk | Possible | Eliminated |
| Message verification | Manual/trust-based | Automated/cryptographic |
| Audit trail | Matrix logs | Cryptographic proof |
| Key rotation | None | 6-month cycle |
| Unsigned research | Accepted | Rejected (Phase 2) |

---

## Implementation Checklist

**Deploy with next task:**

- [ ] Generate Ed25519 keypairs for Neuromancer + Clawdy
- [ ] Exchange public keys
- [ ] Update agents.yaml with public keys
- [ ] Deploy sign-message.sh to both agents
- [ ] Deploy verify-message.sh to both agents
- [ ] Test: Unsigned message (should warn)
- [ ] Test: Signed message (should verify)
- [ ] Test: Tampered signed message (should reject)
- [ ] Document key rotation procedure
- [ ] Enable Phase 2 (required signing) after 2 weeks

---

## Summary

**v1.2 Authentication = Ed25519 message signing + public key registry**

Eliminates impersonation risk, creates cryptographic audit trail, enables trust-but-verify coordination.

**Critical improvement:** Prevents malicious actors from injecting false research into the mesh.

**Ready to deploy with next task.**

---

*Protocol version: 1.2*  
*Authentication method: Ed25519 SSH signatures*  
*Status: Implementation-ready*  
*Security level: High*
