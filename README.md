# Contrarian Agent for Claude Code

A devil's advocate analyst agent for [Claude Code](https://docs.anthropic.com/en/docs/claude-code). It stress-tests proposals by challenging assumptions. Use it for pre-mortem analysis, architecture reviews, decision validation, or whenever consensus feels too easy.

This agent focuses on strategy, approach, and hidden risks. It won't review your code.

## Inspiration

I built this on top of the [Contrarian agent from Ouroboros](https://github.com/Q00/ouroboros/blob/main/src/ouroboros/agents/contrarian.md). The original provides a lightweight assumption-challenging framework. This version extends it with structured output (steel-man, severity-rated findings, verdicts), anti-patterns to avoid, and a calibration system that scales analysis intensity to the stakes.

## Installation

Copy `.claude/agents/contrarian.md` into your project's `.claude/agents/` directory:

```bash
mkdir -p your-project/.claude/agents
cp .claude/agents/contrarian.md your-project/.claude/agents/
```

Or copy it to your user-level agents directory for global availability:

```bash
cp .claude/agents/contrarian.md ~/.claude/agents/
```

## Usage

The agent is available as a subagent in Claude Code. You can invoke it directly:

> "Run the contrarian agent against this proposal"

> "Get a devil's advocate take on this architecture"

## Customizing the Delegation Section

The agent's **Scope > Not in scope** section defines which concerns it defers to other specialists. The generic version ships with broad categories:

```markdown
**Not in scope** (defer to specialists):
- Code review, style, or formatting → code review agents
- Implementation details → domain-specific developer agents
- Infrastructure specifics → infrastructure/platform agents
```

I'd recommend customizing this per project to point at the specific agents available. For example, in a Laravel + GCP project the delegation section might look like:

```markdown
**Not in scope** (defer to specialists):
- Code quality, style, or formatting → `code-reviewer`
- Spec/requirements compliance → `spec-reviewer`
- CSS/frontend implementation → `bulletproof-frontend-developer`
- PHP/Laravel implementation details → `laravel-backend-developer`
- GCP infrastructure specifics → `gcp-architect`
```

This keeps the contrarian agent focused on challenging assumptions and strategy. Implementation-level concerns get routed to agents that have the domain context to handle them. Tweaking this per project ensures you get a tailored set of tools rather than a generic configuration.

## License

[Unlicense](UNLICENSE)
