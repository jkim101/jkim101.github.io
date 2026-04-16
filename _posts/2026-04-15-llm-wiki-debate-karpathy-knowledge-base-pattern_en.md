---
title: "LLM Wiki 찬반 논쟁: Karpathy의 지식 베이스 패턴 분석"
date: 2026-04-15 22:24:23 -0400
categories:
  - blog
tags:
  - LLM Wiki
  - Andrej Karpathy
  - RAG 한계
  - 지식 베이스 패턴
  - LLM 환각
  - 개인 지식 관리
  - PKM
  - 컴파운드 지식
  - 위키 아키텍처
layout: single
author_profile: true
read_time: true
comments: false
share: false
related: true
---

# LLM Wiki: The LLM-Maintained Personal Knowledge Base Pattern — A Deep Dive into the Debate and Practical Implementation

## TL;DR — 3-Minute Summary

The **LLM Wiki** pattern proposed by Andrej Karpathy represents a fundamental shift beyond traditional RAG (Retrieval-Augmented Generation) approaches. Instead of rediscovering knowledge with every query, it creates a persistent wiki artifact that the LLM progressively builds and maintains—a "compiled knowledge" approach.

**Key Takeaways:**
- **Architecture**: Three-tier structure (Raw Sources → Wiki → Schema) with an Ingest-Query-Lint workflow enabling compound knowledge accumulation
- **Pro Arguments**: Compound knowledge effects, maintenance automation, automatic cross-referencing, and realization of Vannevar Bush's Memex vision
- **Con Arguments**: Risk of hallucination contamination, scalability questions regarding context window limits, quality control challenges for auto-generated content, and complexity of human oversight
- **Realistic Assessment**: Best suited for medium-scale knowledge bases (~100 sources, hundreds of pages), with careful attention to domain characteristics and human review

This article provides a balanced analysis of both perspectives, implementation methods, and adoption guidelines.

---

## 1. Introduction: The Limits of RAG and the "Compiled Knowledge" Proposition

### The Problem: Knowledge Retrieval That Forgets Every Morning

Imagine reading the same book from scratch every morning, remembering nothing from yesterday. This is how most RAG systems work today.

When you upload documents to systems like NotebookLM, ChatGPT file uploads, or most RAG implementations, the LLM retrieves relevant chunks each time and generates fresh answers. There's no **accumulation**—no learning, no compound effects.

AI researcher Andrej Karpathy addressed this fundamental issue in his GitHub Gist "[LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)":

> Requiring LLMs to rediscover knowledge from raw sources for every query is fundamentally inefficient—akin to reinventing the wheel thousands of times over.

### Current RAG: Stateless by Design

Traditional RAG follows a simple pipeline:

1. **Chunk**: Convert documents into embeddings
2. **Retrieve**: Find relevant chunks for each query
3. **Generate**: Insert chunks into context and produce an answer
4. **Forget**: When the conversation ends, everything is lost

This works for one-off Q&A but fails for:

- **Cross-document synthesis**: "How do these three papers contradict each other?"
- **Knowledge evolution**: Adding new sources doesn't update previous understanding
- **Maintenance overhead**: Humans must manually curate summaries, tags, and connections

### LLM Wiki's Transformation: From Retrieve-and-Generate to Compile-Once, Keep-Current

Karpathy proposes a fundamental inversion:

**What if the LLM maintained a living wiki like a codebase—compiling knowledge once, keeping it current, and letting insights compound over time?**

This transforms the LLM from a stateless answer machine into a **stateful knowledge architect**.

```
Traditional RAG:           LLM Wiki:
Source → [LLM] → Answer    Source → [LLM] → Wiki → [LLM] → Answer
    ↑______________|            ↑________|      ↑______|
   (Reset every query)      (Wiki persists and compounds)
```

The wiki becomes a persistent artifact—version-controlled, human-inspectable, and progressively smarter with each added source.

---

## 2. Dissecting the LLM Wiki Pattern: Three-Tier Architecture and Core Workflows

### The Three-Tier Architecture

Karpathy's design separates concerns into three layers:

#### Tier 1: Raw Sources (Immutable Truth)
- **What**: PDFs, videos, web pages, Slack logs, meeting notes—everything the LLM learns from
- **Role**: Ground truth that the LLM never modifies
- **Storage**: Local files, cloud storage, version control (Git LFS for large files)

**Example directory structure:**
```
raw/
├── papers/
│   ├── attention_is_all_you_need.pdf
│   └── gpt3_paper.pdf
├── videos/
│   └── karpathy_llm_wiki_talk.mp4
└── web/
    └── hacker_news_discussion.html
```

#### Tier 2: Wiki Pages (LLM-Owned Markdown)
- **What**: Focused markdown files, each hundreds to thousands of words
- **Role**: Compiled, structured knowledge with cross-references
- **The LLM writes and maintains these**—not humans

**Example directory structure:**
```
wiki/
├── index.md              # Content catalog
├── log.md                # Chronological change record
├── transformer_architecture.md
├── attention_mechanisms.md
└── gpt_family_evolution.md
```

**Example Wiki Page Structure:**

```markdown
# Transformer Architecture

**Last Updated**: 2024-12-15  
**Sources**: `papers/attention_is_all_you_need.pdf`, `videos/karpathy_llm_wiki_talk.mp4`

## Overview
The Transformer revolutionized NLP by replacing recurrence with self-attention...

## Core Components
- **Multi-Head Attention**: See [[attention_mechanisms]]
- **Positional Encoding**: Critical for sequence order
- **Feed-Forward Networks**: Applied position-wise

## Evolution
The original architecture spawned [[gpt_family_evolution]]. Key improvements include:
- Layer normalization placement (Pre-LN vs Post-LN)
- Rotary positional embeddings (RoPE)
- Attention optimization techniques

## Open Questions
- How does attention scale to 1M+ token contexts?
- Trade-offs between dense vs. sparse attention patterns

## Related Pages
- [[attention_mechanisms]]
- [[gpt_family_evolution]]
- [[scaling_laws]]
```

#### Tier 3: Schema (The Constitution)
- **What**: A document (e.g., CLAUDE.md for Claude Code or AGENTS.md for Codex) defining wiki structure
- **Role**: Specifies directory rules, page templates, workflows, and update protocols
- **Human-authored**, LLM-executed

**Example Schema Structure:**

```markdown
# Wiki Schema

## Directory Structure
- `raw/`: Never modify. Append-only.
- `wiki/`: LLM owns. Update freely.
- `index.md`: Catalog of all pages. Must link every wiki page.
- `log.md`: Append-only record of ingests, queries, and lint passes.

## Page Template
Every wiki page must include:
- Frontmatter: `title`, `updated`, `sources`
- Sections: Overview, Details, Related Pages
- Cross-references: Use `[[page_name]]` syntax

## Ingest Workflow
When processing new sources:
1. Read source content
2. Identify relevant pages to update
3. For each page:
   - Extract relevant insights
   - Add cross-references
   - Update frontmatter
4. Append to log.md with timestamp and source title

## Query Workflow
1. Start with index.md for topic discovery
2. Follow cross-references
3. If new insights emerge, update relevant pages
4. Log query and updates

## Lint Pass
Periodically check for:
- Orphaned pages (not in index.md)
- Broken links
- Contradictions between pages
- Missing cross-references
```

### The Three Core Workflows

#### 1. Ingest: Absorbing New Knowledge
**Process**:
- LLM reads a new source (e.g., a research paper)
- Identifies relevant existing wiki pages to update (a single source might touch 10-15 pages)
- Extracts insights, adds cross-references, updates metadata
- Appends entry to `log.md`

**Example Log Entry Format:**
```markdown
## [2024-12-15] ingest | Research Paper Title

Updated pages:
- [[page_one]]: Added new insights on topic X
- [[page_two]]: Expanded section on methodology
- [[page_three]]: Created new section on findings
- Created [[new_page]]: Initial analysis of novel concept
```

**Key Insight**: Unlike RAG's "chunk-and-forget," ingestion **permanently enriches** the wiki. The 10th paper on a topic doesn't just answer queries—it deepens existing pages with comparative analysis.

#### 2. Query: Interactive Exploration
**Process**:
- User asks a question
- LLM starts with `index.md` to locate relevant topics
- Follows cross-references across pages
- Synthesizes answer
- If new insights emerge, updates relevant pages
- Logs the query and any updates

**Example Query Workflow:**
```
User: "How do modern attention mechanisms improve efficiency?"

LLM Process:
1. Checks index.md → finds [[transformer_architecture]]
2. Follows link to [[attention_mechanisms]]
3. Discovers relevant optimization section
4. Synthesizes answer from multiple pages
5. Updates pages if new connections emerge
6. Logs the query for future reference
```

#### 3. Lint: Quality Maintenance
**Process**:
- Periodic automated checks for:
  - **Orphaned pages**: Wiki pages not linked in `index.md`
  - **Broken links**: `[[page_name]]` pointing to non-existent pages
  - **Contradictions**: LLM scans for conflicting statements
  - **Missing cross-references**: Topics mentioned but not linked

**Example Lint Output:**
```markdown
## [2024-12-15] lint pass

Issues found:
- Orphaned page: [[deprecated_concepts.md]]
- Broken link in [[main_topic]]: [[nonexistent_page]] does not exist
- Potential contradiction detected between [[page_a]] and [[page_b]]
- Missing cross-reference in [[topic_x]] to related [[topic_y]]
```