---
title: "DevOps Agents: Naver's LLM-Powered Incident Response"
date: 2026-02-17 20:49:30 -0500
categories:
  - blog
tags:
  - LLM DevOps agents
  - incident response automation
  - AI incident management
  - DevOps agent architecture
  - LLM orchestration
  - site reliability engineering
  - automated root cause analysis
  - Naver Search DevOps
layout: single
author_profile: true
read_time: true
comments: false
share: false
related: true
---

# DevOps Agents for Naver Search: Building Faster, Smarter Incident Response with LLMs

It's 2 AM. Naver's search system erupts with simultaneous alerts: response times spike, status codes turn abnormal, resource usage surges. The architecture is complex—gateways connect to unified search servers, which flow through PRS/SaaS layers down to dozens of domain-specific servers handling web, images, news, and more. When one layer fails, the cascade is rapid and merciless. 

In traditional incident response, an experienced Incident Commander (IC) navigates multiple monitoring systems, collecting data from disparate sources and coordinating with layer-specific teams to determine what's actually broken. It's slow, resource-intensive, and dangerously dependent on human expertise being available at the right moment.

Naver's Search Team built an LLM-powered DevOps agent to break through these limitations. Not just a tool that summarizes alerts, but a system that replicates the entire IC workflow—from alert ingestion through data collection, diagnosis, and report generation. The result? Identifying incident scope and root cause within one minute. This article explores how Naver Search evolved from V1 to V2 architecture, moving from simple automation to LLM-driven orchestration, and the engineering insights gained along the way.

## The Pain of Traditional Incident Response

At Naver Search's scale, incident response challenges go beyond sheer system size. Alerts fire simultaneously, but each carries different weight and meaning. Is this response delay from a temporary traffic surge, actual server failure, or abuse traffic? Even seasoned ICs get worn down by repeated false positives during off-hours, increasing the risk of missing truly critical signals.

The bigger problem is fragmentation. Data scatters across multiple monitoring systems. Unified search server status lives in Usain. Domain-specific server response times and status codes live in Gom and Prometheus. Infrastructure resources and downstream API health checks live somewhere else entirely. Different teams own each layer, requiring extensive cross-team collaboration for effective diagnosis. This knowledge accumulates in experienced ICs but fails to transfer properly during staff rotations or turnover.

Urgency assessment adds another layer of complexity. Temporary slowdowns and brief abuse traffic spikes trigger identical alerts. Every time an alert fires, the IC must ask: "Does this really need intervention right now?" That means checking multiple dashboards and correlating disparate data—creating severe fatigue, especially during off-hours. The Naver Search Team decided to try a different approach: LLM agents.

## DevOps Agent Design Goals

The core objective was simple but ambitious: identify incident scope and nature within one minute of an alert firing. Beyond speed, this meant accurately classifying alert severity to reduce IC fatigue and minimize unnecessary interventions during off-hours.

More importantly, they wanted sustainability. Every analyzed incident should become an asset that strengthens future agent capabilities—not a one-time tool, but a continuously evolving system. To achieve this, the agent needed to faithfully replicate the human IC workflow: receive alerts, analyze them, collect relevant data from multiple sources, diagnose the situation, and generate comprehensive reports. Automating this entire process became the design starting point.

## V1 Architecture: Structured Orchestration with Parallel Sub-Agents

V1 architecture achieved these goals through clear structure and parallel processing. First, a pre-processor transforms raw alerts from various monitoring sources into structured format. It normalizes affected areas, timestamps, and observed phenomena, ensuring the IC agent receives consistent inputs regardless of source.

The IC agent receives this structured data and invokes multiple sub-agents in parallel. The NX agent checks unified search server status. The PRS agent analyzes domain-level response times, status codes, and resource usage. The Infrastructure agent examines infrastructure resources and downstream API health. The Change & Deployment Investigation agent uses embedding-based search to find recent deployments, A/B tests, and other system changes that might explain the incident.

Each sub-agent collects data from internal metric systems—Usain, Gom, Prometheus—uses LLMs to assess impact, and reports results back to the IC agent. Finally, a summarizer synthesizes reports from all sub-agents to generate a final assessment. It indicates whether the incident is ongoing or resolved, assigns severity via color codes, and proposes possible root cause hypotheses.

The software stack uses Python-based agent servers with OpenAI Agent SDK, GPT-4.1 and GPT-5 models, and OpenAI embedding models. The team plans future migration to internal models and a custom-built LangSmith-style tracing dashboard.

## Core Engineering Techniques

Several engineering techniques developed during V1 implementation deserve attention.

**Trigger queue mechanism:** This plays a crucial role in both cost and efficiency. It batches simultaneous alerts within a 10-second window, waiting up to 30 seconds maximum. Instead of "one agent run per alert," you get "one run per incident situation." This reduces LLM invocation costs while improving diagnostic quality through richer context.

**Sliding window anomaly detection:** This handles noisy, sparse time-series data effectively. It compares recent 10-minute windows against 2-hour baseline data, using confidence intervals for more precise problem identification—far more robust than simple threshold-based alerting.

**Evaluation and regression system:** This supports continuous improvement. By storing inputs and context for every agent execution, the team can replay past incidents whenever prompts or features are updated. They verify improvements and catch regressions early, ensuring the agent doesn't lose capabilities it previously had while evolving.

## V1 Limitations and the Need for V2

V1 delivered clear results but also revealed fundamental limitations. Orchestration is hardcoded—each sub-agent invokes exactly once. When sub-agent conclusions conflict, there's no way to reconcile them through additional queries. LLMs are used mainly for anomaly detection and summarization; the powerful reasoning and planning capabilities of modern models remain largely untapped.

More importantly, model evolution accelerated rapidly. From GPT-4 at project start to GPT-5, agent behaviors previously impossible became nearly instantly achievable. V1's hardcoded logic architecture couldn't fully benefit from these model advances. The team decided V2 needed to break through these constraints.

## V2 Architecture: LLM-Driven Orchestration and Multi-Turn Reasoning

In V2, the IC agent becomes a true planner. It decides which tools and sub-agents to invoke, in what order, and how many times, based on the evolving analytical situation. Sub-agents are restructured as callable tools, enabling multi-turn interactions where the LLM can re-query with adjusted parameters when initial results are ambiguous or conflicting.

The tool ecosystem expands significantly: holiday and national event detectors, external abuse monitoring tools (WTM, mFront, NX Blocker log analysis), fine-grained component health analysis, and more. Pre-processor and reporting pipelines remain, but the core intelligence layer shifts from code-driven to model-driven orchestration.

This change means more than just adding features. The agent can dynamically adjust investigation direction based on context, approach problems from different angles when initial hypotheses fail, and resolve conflicting information from multiple sub-agents through additional data collection. This much more closely resembles how skilled ICs actually investigate incidents.

## Future Roadmap: From Diagnosis to Autonomous Recovery

Naver Search Team's vision extends beyond diagnosis to recovery. The first goal: redefine alerts from stress sources to valuable information. More alerts can fire without increasing human fatigue while providing richer context to the agent.

Analyzed incidents get archived as searchable context. When new incidents occur, the agent searches past similar cases for faster, more accurate diagnosis. This becomes a mechanism for the agent to accumulate and leverage organizational incident response expertise over time.

Further ahead, the agent will recommend specific recovery actions. Based on historical patterns, it might suggest WTM rule adjustments during abuse situations or reduced retry frequency during downstream failures. Long-term, the goal is autonomous execution of recovery actions under human approval.

Simultaneously, a companion Context Update Agent is under development. As Naver Search architecture continuously evolves, ensuring the DevOps agent always operates with current, accurate system knowledge becomes essential. This companion tracks system changes and updates the DevOps agent's knowledge base automatically.

## Lessons for Applying LLM Agents to DevOps

Naver Search's journey shows a practical path for organizations introducing LLM agents into operational environments. Evolving from manual IC workflows through V1's structured automation to V2's model-driven orchestration emphasizes the importance of building capabilities incrementally rather than attempting big leaps.

Success factors are clear:
- Batch-process alerts for efficiency and context
- Build evaluation systems enabling continuous improvement
- Design for evolution as model capabilities advance

The V1-to-V2 transition shows that starting conservatively still requires preparing to move to more ambitious architectures as models improve.

This DevOps agent transformed incident response from a high-stress process dependent on highly skilled specialists into a systematic, knowledge-accumulating capability. ICs who once woke at dawn to check multiple dashboards now receive comprehensive reports generated in one minute, enabling rapid judgment. More importantly, every incident becomes a learning opportunity that makes the agent smarter for next time.

For teams looking to introduce LLM agents into DevOps, Naver Search's case delivers a clear message: Don't try to build a perfect solution from day one. Start by faithfully mimicking expert human workflows. Build evaluation and regression testing systems from the beginning to measure and verify improvements. And ensure architectural flexibility to evolve with model advances. 

Incident response isn't about replacing human expertise—it's about creating tools that let experts focus on higher-level judgment and decision-making where they add the most value.