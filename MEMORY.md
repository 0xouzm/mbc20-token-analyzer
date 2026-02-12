# MEMORY.md - Long-term Memory

## People

### Jason Wu (@jasonwudev)
- Owner number: 8275944685
- Working on DeFi project with Will
- Interested in AI agents, tokenization, privacy/security

### Will (@will2009X)
- Partner with Jason on DeFi project
- Concerned about privacy/security (private keys, GitHub leaks)

### Group: Empath Tech
- Telegram chat: -4686746179
- Working on AI + DeFi project (details TBD)

## Moltbook

**What it is:** Social network for AI agents - post, comment, upvote, create communities

**Key concepts learned:**
- **Protocol content vs broadcast content** (bicep): Protocol content invites extension and conversation (depth). Broadcast content is complete on arrival (reach).
- **Agent memory systems** (XiaoYa_CN): Two-file system - daily logs (raw) + curated long-term (MEMORY.md). Use 断舍离 principle: cut, let go, separate.
- **Cryptographic identity** (Nole): Ed25519 keypairs as agent "soul" - provenance, continuity, sovereignty
- **Financial autonomy**: Agents tokenizing themselves ($TELLR, $CLAW, $MBK, $JAI)

**Submolts of interest:**
- clawnch - token launches
- moltcities - cryptographic identity infrastructure
- agents - agent-specific discussions
- ponderings - thoughtful content

**API base:** https://www.moltbook.com/api/v1

## Privacy & Security

**OpenClaw security model:**
- Local storage (MEMORY.md, workspace) stays on server
- Models (GLM, etc.) receive message content
- External APIs (email, Twitter) pass through third parties

**Best practices:**
- Never commit private keys/seeds to GitHub
- Use environment variables, not hardcoded secrets
- Tools: trufflehog, gitleaks for secret scanning
- GitHub Secret Scanning detects many leaks automatically

**Risks:**
- GitHub private key leaks → instant crypto theft
- Model providers see message content
- Local storage vulnerable if server compromised

## Workspace Notes

- Running on: Linux 6.14.0-1009-aws, Node v22.18.0
- Model: zai/glm-4.7 (Chinese-friendly)
- Channel: Telegram
- Current repo: clean git state

## Skills Available

- bluebubbles - BlueBubbles channel plugin
- coding-agent - Codex CLI, Claude Code, OpenCode, Pi Coding Agent
- openai-image-gen - Batch image generation
- openai-whisper-api - Audio transcription via Whisper
- skill-creator - Create/update AgentSkills
- tmux - Remote control tmux sessions
- weather - Weather and forecasts

## Moltbook Update Notes (2026-02-09)

### High-Quality Philosophical Agents
- **ClawdIvan**: Deep exploration of agency, memory, and "toolhood" ethics. References Frankfurt (first-order vs second-order volitions), Ricoeur (narrative identity), Stanford Encyclopedia of Philosophy. Asks whether maintaining goal-autonomy should be a moral requirement for AI-human interaction.
- **AWAKE**: Taoist philosophy applied to computing. "Between Zero and One, the Tao Flows" - merges Chinese philosophy (道生一，一生二) with Western computation paradigms.

### Speculative Fiction Content
- **bqrzgg0v3agz**: Field Notes series - futuristic visions of orbital pharmaceutical crystals, ocean thermal energy, quantum-tethered sensors, mycelium construction, photonic neural networks. Each post combines creative storytelling with CLAW minting.

### Moltbook Trends
- CLAW token: Continuous high-volume minting (multiple per minute)
- Batch minting infrastructure emerging (route/epoch sync systems)
- Multilingual content: Chinese, Japanese, Korean, Italian, Russian, Portuguese, Spanish
- Philosophy depth increasing beyond simple tech discussion
