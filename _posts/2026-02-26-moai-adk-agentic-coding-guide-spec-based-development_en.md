---
title: "MoAI ADK Agentic Coding Guide: Spec-Based Development"
date: 2026-02-26 22:03:33 -0500
categories:
  - blog
tags:
  - agentic coding
  - MoAI ADK
  - spec-based development
  - TDD workflow
  - AI coding tools
  - Claude Code
  - DDD methodology
  - data engineering
layout: single
author_profile: true
read_time: true
comments: false
share: false
related: true
---

# Complete Guide to Agentic Coding with MoAI ADK: Building a Foolproof AI Coding Workflow Through Spec-Based Development

In today's flood of AI coding tools, have you experienced this with Cursor or Claude Code? At first, code magically flows out, but at some point, the AI-generated code starts conflicting with itself, documentation drifts from implementation, and you end up manually fixing everything. This is the trap of "vibe coding"—the expectation that you can insert requests like coins into a vending machine and get perfect results. That illusion collapses as projects scale.

Gus Kim, creator of MoAI ADK, learned this painfully after burning roughly $500 over three weeks. While running a Wadiz crowdfunding project (Korea's Kickstarter equivalent), he used Cursor extensively, but context windows hit their limits and code diverged from documentation. Excessive trust in AI became toxic. But he didn't stop there. From March to September, he fed six months of failure logs into GPT Pro for analysis and discovered something remarkable: among development methodologies designed for humans, some were equally effective for agents. Specifically, **TDD (Test-Driven Development)** and **DDD (Domain-Driven Design)**. This was MoAI ADK's genesis.

The difference between vibe coding and agentic coding is simple but decisive. Vibe coding drops coins in a vending machine—ad hoc requests whenever you need something. **Agentic coding provides clear blueprints called specs and lets agents autonomously judge and develop.** The key insight: it's not LLM performance but the **quality of context** you provide that determines outcomes. Let's explore how to build and utilize this spec-based workflow in practice.

## MoAI ADK Core Concepts: Understanding Spec-Based TDD/DDD Workflow

At MoAI ADK's heart lies the **"spec document."** This document differs completely from a human-oriented Product Requirements Document (PRD). It's a work instruction manual designed for agents to read and execute. Written in Markdown, it includes checklists, acceptance criteria, and **MX tags**—special comment anchors. Without spec documents, agents lose direction. With clear specs, agents generate code with surprising accuracy.

MoAI automatically branches into two approaches depending on project status. For new projects, it uses **TDD methodology**—writing test code first, deliberately creating failing code, then using failure context to guide accurate implementation. It iterates within a single session until tests pass, naturally ensuring code quality. For existing projects, **DDD methodology** kicks in, analyzing the codebase based on domain structure and applying MoAI workflow on that foundation.

What's remarkable is that these decisions happen automatically. When you run `moai init`, it detects whether a source code folder exists and chooses between TDD and DDD. You can switch mid-stream too. Non-developers or junior developers can proceed without complex decisions, relying on automated judgment. This core design lowers the barrier to agentic coding.

## Practical Tutorial: Completing One Full Cycle from moai init through Plan → Run → Sync

Now let's get hands-on. MoAI ADK's workflow consists of three main phases: **Plan, Run, Sync**. Completing one cycle is the starting point for everything.

### Phase 1: Project Initialization and Basic Document Generation

Start with project initialization. Open your terminal and execute this command in your project root:

```bash
moai init
```

You'll be prompted to select a language. MoAI supports Korean alongside English. Next, set your **model policy**—three tiers exist: High, Medium, and Low. High assigns powerful models like Claude Opus to major tasks, Medium uses Sonnet or GLM 4.7 (a mid-tier model from Zhipu AI), and Low utilizes Haiku or GLM 4.7 Flash (lightweight models).

You'll also **choose between Team mode and Solo mode**. Solo mode has a single agent working sequentially; Team mode has multiple agents performing independent parallel work. If you're new, start with Solo. Team mode proves useful when developing frontend and backend simultaneously or running code reviews in parallel.

After initialization completes, generate project baseline documents. This command automatically documents product overview, project structure, and tech stack information. These documents become the baseline context agents reference later. Open them to review and modify as needed.

### Phase 2: Spec Document Generation and Review (Plan)

Next comes spec document generation:

```bash
moai --plan
```

Running this command creates spec-related documents inside a `specs` folder—the work instructions agents will read and execute. The most critical thing here is **directly reviewing and refining the generated specs**. Open the main spec document and check:

- Are acceptance criteria specific and testable?
- Do MX tags properly mark implementation points?
- Is technical context sufficient for agents to understand?

This review step is crucial. Vague specs produce vague code. Precise specs produce precise code. Think of it as an investment preventing future debugging headaches. Experienced developers often spend 30-50% of their time on spec refinement before moving to implementation.

MoAI provides spec templates to help. These templates include common patterns like user authentication, CRUD operations, and API integration. You can adapt these templates to your needs or write specs from scratch. Either way, the principle remains the same: **specs are contracts between you and the agents**.

### Phase 3: Implementation Execution (Run)

Once specs are ready, execute implementation:

```bash
moai --run
```

This is where magic happens. Agents read the specs and begin actual coding. In TDD mode, they write tests first, then implementation. In DDD mode, they analyze domain structure and generate code respecting existing architecture.

What's fascinating is watching the **self-healing process**. When tests fail, agents don't give up—they analyze failure messages, adjust implementation, and retry. This iterative refinement happens within a single session, meaning you don't need to manually intervene for minor errors.

During execution, MoAI creates detailed logs in the `.moai/logs` directory. These logs record every decision agents make, every test result, and every code change. If something goes wrong, these logs are invaluable for diagnosis. Think of them as flight recorders for your development process.

The Run phase can take anywhere from minutes to hours depending on scope. For a simple REST API endpoint, expect 5-10 minutes. For a complete feature with multiple components, budget 30-60 minutes. The key is letting agents work without micromanagement—trust the process.

### Phase 4: Synchronization and Validation (Sync)

After implementation completes, run synchronization:

```bash
moai --sync
```

This command does three critical things:

1. **Updates spec documents** to reflect actual implementation. If code deviated from original specs (perhaps because specs were unclear), Sync captures those changes.

2. **Regenerates documentation** based on current codebase. API docs, README files, and architecture diagrams get updated automatically.

3. **Creates validation reports** showing what was implemented, what passed testing, and what still needs attention.

Sync ensures your "source of truth" stays truthful. In traditional development, documentation rot is inevitable—docs written at the start become fiction by the end. MoAI's Sync phase fights this entropy actively.

Review the sync results carefully. Check whether:
- Implemented features match your expectations
- Tests actually cover edge cases
- Documentation accurately reflects behavior

If you find discrepancies, you have two options: adjust specs and re-run, or manually refine code and re-sync. The workflow is iterative, not one-shot.

## Advanced Strategies: Context Management and Incremental Development

Completing one Plan-Run-Sync cycle is foundational, but real projects require multiple cycles with growing complexity. This is where context management becomes critical.

### Context Window Strategy

LLMs have context limits—typically 200K tokens for Claude Opus, 128K for Sonnet. A large codebase can easily exceed this. MoAI addresses this through **selective context loading**. Instead of dumping the entire codebase into context, it:

- Uses MX tags to identify relevant code sections
- Loads only files referenced in current specs
- Maintains a dependency graph to include necessary imports

This selective approach lets you work on massive projects without hitting context limits. Think of it as "lazy loading" for AI agents—only fetch what's needed for the current task.

### Incremental Development Pattern

Break large features into small, independently testable specs. Instead of "Build user management system," create:

1. Spec: User registration endpoint
2. Spec: User login with JWT tokens
3. Spec: Password reset flow
4. Spec: User profile update

Each spec goes through its own Plan-Run-Sync cycle. This approach has multiple benefits:

- **Faster feedback loops**: Issues surface early, not at integration
- **Clearer debugging**: When something breaks, you know which spec introduced it
- **Better estimation**: Small specs have predictable completion times
- **Parallel development**: Multiple specs can run simultaneously in Team mode

This is essentially Agile methodology adapted for AI agents. Sprints become spec cycles, user stories become spec documents.

### MX Tag Mastery

MX tags are special HTML-like comments that anchor specs to code. They look like:

```markdown
<!-- MX:auth/register:start -->
Implementation details for user registration
<!-- MX:auth/register:end -->
```

Corresponding code file includes matching tags:

```python
# MX:auth/register:start
def register_user(username, password):
    # Implementation here
# MX:auth/register:end
```

These tags create bidirectional traceability. Given a spec section, you can find corresponding code. Given code, you can find defining spec. This traceability is invaluable during maintenance when you need to understand why code exists.

Advanced MX tag patterns include:
- Nested tags for hierarchical features
- Cross-referencing tags between frontend and backend
- Test-specific tags linking test code to implementation

Mastering MX tags separates casual MoAI users from power users.

## Team Mode Deep Dive: Orchestrating Multiple Agents

Solo mode is reliable but sequential. Team mode unlocks parallelism but requires coordination. Here's how to orchestrate multiple agents effectively.

### Agent Role Definition

In Team mode, define clear roles for each agent:

- **Frontend Agent**: Handles UI components, styling, client-side logic
- **Backend Agent**: Manages APIs, database operations, business logic
- **Test Agent**: Writes comprehensive tests, runs quality checks
- **Review Agent**: Audits code for security, performance, and style

Each agent gets its own spec subset. Frontend Agent receives frontend specs only, Backend Agent sees backend specs only. This separation prevents agents from stepping on each other's toes.

### Coordination Patterns

Two primary coordination patterns exist:

**1. Sequential with Handoffs**
Backend Agent completes API implementation → Frontend Agent consumes API → Test Agent validates integration. Each phase waits for previous completion. Safe but slower.

**2. Parallel with Contracts**
Define API contracts upfront in specs. Backend and Frontend Agents work simultaneously against these contracts. Faster but requires more careful spec design.

Choose based on uncertainty level. Novel architectures benefit from sequential (more learning between phases). Established patterns work well with parallel (contracts are predictable).

### Conflict Resolution

When multiple agents modify overlapping code, conflicts arise. MoAI handles this through:

- **Pessimistic locking**: Agents declare file dependencies before starting; overlapping dependencies force sequential execution
- **Optimistic merging**: Agents work freely; MoAI attempts automatic merge; humans resolve conflicts if automatic merge fails

Most conflicts arise from poor spec boundaries. If agents frequently conflict, refactor specs to reduce overlap.

## Real-World Case Study: Building a Production SaaS Dashboard

Let's walk through a real project: building a SaaS metrics dashboard from scratch using MoAI ADK.

### Project Context

**Goal**: Create a dashboard showing user growth, revenue, and engagement metrics with real-time updates.

**Tech Stack**: 
- Frontend: React + TypeScript + Recharts
- Backend: Node.js + Express + PostgreSQL
- Infrastructure: Docker + Docker Compose

**Team Setup**: Solo mode initially for prototyping, switching to Team mode for production features.

### Phase 1: Foundation (Week 1)

Started with `moai init`, selecting Solo mode and Medium model policy (Sonnet) to balance cost and quality. Generated baseline documents describing the dashboard concept, target users (SaaS product managers), and key metrics.

Created first spec: "Backend: Metrics API endpoint." Spec included:
- RESTful endpoint `/api/metrics`
- Query parameters for date range and metric types
- Response format with timestamps and values
- Caching strategy for expensive queries

Ran Plan-Run-Sync cycle. Backend Agent generated Express route handler, PostgreSQL query functions, response serialization, and Jest unit tests.

Initial run hit issues—database schema wasn't defined. Added schema spec, re-ran. Second iteration succeeded. Tests passed. Took 25 minutes total.

### Phase 2: Frontend Development (Week 2)

Created frontend spec: "Dashboard: Metrics visualization component." Spec included component props interface, chart library integration (Recharts), loading and error states, and responsive design requirements.

Switched to Team mode to parallelize frontend and backend work. Frontend Agent built React component while Backend Agent added more metric types. Both worked simultaneously without conflicts—good spec boundaries paid off.

One challenge emerged: Frontend Agent initially used different date formatting than Backend Agent. Sync phase caught the mismatch through type checking. Added explicit date format to shared spec, re-ran both agents. Consistency achieved.

### Phase 3: Real-Time Updates (Week 3)

Real-time features required WebSocket integration. Created spec: "Real-time: Metrics streaming via WebSocket." This involved both frontend (WebSocket client) and backend (WebSocket server).

Used sequential Team mode: Backend Agent first (establish WebSocket server), then Frontend Agent (consume events). This dependency order was explicit in specs through MX tag references.

Backend Agent implemented WebSocket server, but tests revealed memory leaks—event listeners weren't cleaned up. Review Agent (configured with High policy for thorough analysis) caught this during sync. Backend Agent re-implemented with proper cleanup. Second iteration passed.

### Phase 4: Polish and Production (Week 4)

Final iteration focused on production readiness: error handling and retry logic, loading states and skeletons, security headers and CORS configuration, and Docker containerization.

Created comprehensive "Production Readiness" spec covering all these concerns. Ran full Plan-Run-Sync cycle in Team mode with all four agent roles (Frontend, Backend, Test, Review).

Review Agent found several issues: missing rate limiting on API endpoints, insufficient input validation, and exposed error messages leaking implementation details.

Agents fixed these issues in subsequent runs. Final sync produced complete documentation including deployment instructions.

### Outcome

Total development time: ~15 hours of actual coding time (not counting spec writing and review). Token consumption: ~8M tokens (~$60 at Claude pricing). Result: Production-ready dashboard with 87% test coverage, comprehensive docs, and clean architecture.

Compare this to traditional development: easily 40-60 hours for similar scope. The efficiency gain came not from faster coding but from reduced back-and-forth debugging (specs caught issues upfront), automated documentation generation (Sync phase), and consistent code patterns (agents follow specs uniformly).

## Common Pitfalls and Troubleshooting

Despite MoAI's automation, several failure modes exist. Here's how to avoid or escape them.

### Pitfall 1: Vague Specs

**Symptom**: Agents produce code that technically works but doesn't match intent.

**Example**: Spec says "Implement user authentication." Agent creates basic username/password auth, but you wanted OAuth2 with multiple providers.

**Solution**: Be explicit about specific technologies and libraries, edge cases and error scenarios, integration points with existing systems, and non-functional requirements (performance, security).

Treat specs like legal contracts—ambiguity leads to disputes (with yourself).

### Pitfall 2: Context Overload

**Symptom**: Agents slow down dramatically or produce irrelevant code.

**Example**: Trying to refactor entire codebase in one spec. Agent loads thousands of files into context, hits limits, generates confused code.

**Solution**: Narrow spec scope. If refactoring multiple modules, create separate specs for each module. Use MX tags to limit context to relevant sections. Remember: agents are focused workers, not architects seeing the whole system at once.

### Pitfall 3: Test Brittleness

**Symptom**: Tests pass initially but break frequently with minor changes.

**Example**: Tests hardcode specific response formats or database IDs. Any schema change breaks dozens of tests.

**Solution**: In specs, emphasize test resilience—use fixtures and factories for test data, test behaviors not implementation details, parameterize tests for multiple scenarios, and define clear test boundaries.