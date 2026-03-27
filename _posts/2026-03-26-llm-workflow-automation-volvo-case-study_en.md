---
title: "LLM Workflow Automation: Volvo Case Study & Results"
date: 2026-03-26 22:32:27 -0400
categories:
  - blog
tags:
  - LLM workflow automation
  - multidisciplinary software development
  - AI coding automation
  - Volvo Group case study
  - workflow graph modeling
  - API development automation
  - LLM agents
layout: single
author_profile: true
read_time: true
comments: false
share: false
related: true
---

# Revolutionizing Multidisciplinary Software Development with LLM-Based Workflow Automation: A Volvo Group Case Study

## TL;DR

By applying LLM-based workflow automation to Volvo Group's real-world in-vehicle API system, we reduced development time per API from approximately 5 hours to under 7 minutes—over 97% faster—while achieving an F1 score of 93.7%. The key lesson: accelerating individual tasks with AI coding assistants alone isn't enough. To achieve genuine productivity gains, you must model the entire workflow—from domain artifacts to code—as a graph and progressively automate it. This case study presents validated results from a production environment with 192 API endpoints, 420 attributes, and 776 CAN signals. The approach saved approximately 979 hours of engineering effort across the portfolio and earned high satisfaction ratings from domain experts (4.80/5) and developers (4.67/5).

## Introduction: Why AI Coding Assistants Alone Aren't Enough

AI coding assistants like GitHub Copilot have become part of daily life for many developers. Type a function signature, and the assistant completes the body. Describe your intent in a comment, and it suggests matching code. These tools have revolutionized individual developer speed and eliminated repetitive tasks. But do they actually solve the fundamental productivity bottlenecks in real industrial settings?

The reality is more complex. In Multidisciplinary Software Development (MSD) environments, the true bottleneck isn't writing code—it's the translation and coordination between heterogeneous artifacts. In automotive, converting CAN signal specifications into API endpoints; in medical devices, encoding clinical protocols as software constraints; in financial systems, implementing regulatory requirements as validation logic—none of these are about typing code faster. They're complex cognitive tasks involving domain expertise, documentation at various abstraction levels, and translating tacit knowledge from different expert groups into explicit implementations.

Volvo Group's spapi system vividly illustrates these challenges. Spapi is an in-vehicle web server that maps vehicle signals and control states to authenticated RESTful endpoints, enabling application developers to access vehicle status and functionality. The system spans six functional domains—driver productivity, connected systems, energy management, vehicle systems, visibility, and dynamics—each with its own expert community. Energy management specialists care about battery efficiency and charging protocols, while vehicle dynamics experts focus on suspension control and stability algorithms. Each group has its own language, tools, and documentation systems.

Integrating this complexity into software requires 15 to 20 full-time engineers working continuously. While developing and maintaining over 100 API endpoints, engineers constantly interpret domain documents, translate signal definitions into code, coordinate with stakeholders, and track specification changes. Each API required approximately 5 hours of development time, most spent not writing code but searching documents, consulting experts, and resolving inconsistencies. A single API definition could take up to 10 weeks from initial specification to deployment-ready code.

GitHub Copilot can accelerate the code-writing phase, but it doesn't automate the workflow from domain specification to implementation. Engineers must still manually search CAN signal databases, read attribute definition documents, match signals to attributes, and design API endpoint structures. This is why Volvo Group pursued an approach beyond coding assistance—redesigning and automating the workflow itself.

## Four Failure Modes of Multidisciplinary Software Development

As the Volvo Group team analyzed their workflow, they discovered four recurring failure modes in multidisciplinary software development. These patterns aren't limited to automotive—they appear wherever domain knowledge must be encoded in software.

### 1. Fragmented Artifacts

The first is fragmented artifacts. API specifications, signal definitions, detailed descriptions, coordination notes, version histories—each exists in different formats and abstraction levels. OpenAPI specs are structured YAML files, CAN signals are in DBC format, attribute descriptions live on wiki pages, and domain experts' explanations are scattered across issue tracker comments.

These artifacts have different update cycles, owners, and version control schemes. Inconsistency is inevitable. Signal definitions get updated but API specs still reference old versions, or attribute descriptions are current but implementation code reflects outdated assumptions. In the spapi system, with over 400 attributes and 776 CAN signals, maintaining consistency manually becomes a Sisyphean task.

The real cost isn't just search and reconciliation time—it's the cognitive load. Engineers must build and maintain mental models of how these heterogeneous artifacts relate. Which signals map to which attributes? Which API endpoints expose which signals? Which documentation version corresponds to which code version? This mental overhead compounds as the system scales, and when team members change, this implicit knowledge is lost.

### 2. Implicit Workflow Dependencies

The second failure mode is implicit workflow dependencies. API development follows a logical sequence: understand domain requirements, identify relevant signals, map signals to attributes, design endpoint structure, implement code, validate against specifications, and deploy. But in practice, this workflow is rarely documented as an explicit process model.

Instead, it exists as tribal knowledge distributed across the team. Experienced engineers know that before implementing a battery status endpoint, you need to consult both the energy management team's specification documents and the CAN database maintainer, cross-reference signal scaling factors with the vehicle platform documentation, and verify that the proposed endpoint structure aligns with the existing API taxonomy. None of this is written down—it's learned through apprenticeship and repeated mistakes.

The consequence is inconsistent execution. Different engineers follow different paths, leading to varying quality and different types of errors. When specifications change, there's no systematic way to identify which downstream artifacts need updates. The workflow operates like an invisible graph with implicit edges, and each node transition relies on individual judgment.

### 3. Context Switching Overhead

The third failure mode is context switching overhead between domain and implementation spaces. This is where the multidisciplinary nature extracts its heaviest toll. An engineer working on a vehicle dynamics API must shift between fundamentally different conceptual frameworks multiple times within a single task.

At one moment, they're reading domain expert documentation about suspension damping characteristics, understanding concepts like roll stiffness and pitch control. The next moment, they're navigating a CAN signal database looking for specific signal identifiers and bit-level encoding schemes. Then they switch to designing a REST API structure, thinking about HTTP methods, URL patterns, and JSON schema. Finally, they move to implementing code generation templates and validation logic.

Each transition requires loading a completely different mental model. The cognitive cost is substantial—not just in time, but in increased likelihood of errors. Domain concepts don't map one-to-one to implementation constructs. A single domain attribute like "vehicle speed" might derive from multiple CAN signals with complex aggregation logic. An API endpoint's authentication requirements might depend on subtle interpretations of safety regulations. These translations require deep contextual understanding that's difficult to maintain while constantly context-switching.

In Volvo's case, engineers reported that this context switching was one of the most exhausting aspects. The expertise required spans vehicle engineering, embedded systems, networking protocols, API design, and code generation—few individuals possess deep knowledge across all these domains, yet the workflow demands it continuously.

### 4. Manual Synchronization Burden

The fourth failure mode is the manual synchronization burden. In any living system, change is constant. Domain requirements evolve as new vehicle features are added. CAN signal definitions are updated when hardware changes. API design patterns are refined based on developer feedback. Security requirements tighten in response to new threats.

Each change must propagate through the entire artifact chain—from domain specification to signal definitions to API specs to implementation code to test cases. Without automation, this propagation is manual, time-consuming, and error-prone. An engineer must remember to update not just the immediate artifact but all dependent ones.

In practice, this rarely happens perfectly. Partial updates accumulate, creating drift between artifacts. The API specification might reflect the latest requirements, but the implementation code lags behind. Or the code is updated, but the documentation isn't. Over time, this drift compounds, and the system's actual behavior diverges from its documented specification.

Volvo's spapi system, with hundreds of APIs and thousands of signals, faced this synchronization challenge at scale. A single CAN signal modification could require updates across dozens of API endpoints. Tracking these dependencies manually was not just inefficient—it was becoming unsustainable as the system grew.

## The Workflow-First Automation Approach

Recognizing these failure modes, the Volvo Group team adopted a fundamentally different approach: rather than starting with AI code generation, they started with workflow modeling. The core insight was that productivity gains come not from automating individual tasks in isolation, but from automating the coordination and dependencies between tasks.

### Modeling the Pipeline as an Explicit Graph

The first step was making the implicit workflow explicit by modeling it as a directed acyclic graph (DAG). Each node represents a distinct artifact or transformation step:

1. **Domain Requirements**: High-level functional specifications from domain experts
2. **Attribute Definitions**: Structured descriptions of vehicle properties to expose
3. **Signal Mapping**: Identification of CAN signals that provide attribute data
4. **API Design**: Endpoint structure, URL patterns, request/response schemas
5. **Implementation Code**: Generated Python/C++ code for the API server
6. **Validation Logic**: Test cases and constraint checkers
7. **Documentation**: Auto-generated API reference documentation

The edges represent transformations and dependencies. Attribute definitions depend on domain requirements. Signal mapping depends on both attributes and the CAN database. API design depends on attributes and follows design guidelines. Implementation code is generated from API design and signal mappings.

By externalizing this graph, the team achieved several immediate benefits even before automation:

- **Visibility**: The workflow became inspectable—anyone could see the full path from requirements to code
- **Consistency**: All engineers followed the same process, reducing variation in output quality
- **Change Impact Analysis**: When an artifact changed, the graph revealed which downstream nodes needed updates
- **Optimization Targets**: Bottlenecks became measurable—which edges consumed the most time? Which transformations had the highest error rates?

This graph model became the skeleton upon which LLM automation would be built.

### LLM-Based Transformation Agents

With the workflow graph established, the next step was automating individual edges—the transformations between nodes. This is where LLMs entered, but in a highly structured way. Rather than using LLMs as general-purpose code generators, each LLM agent was specialized for a specific transformation task within the graph.

**Attribute Extractor Agent**: This agent takes domain requirement documents (often natural language, sometimes semi-structured) and extracts structured attribute definitions. It identifies what properties should be exposed (e.g., "battery state of charge", "current vehicle speed"), their data types, units, valid ranges, and access permissions.

The agent uses entity extraction, schema mapping, and domain-specific prompting. It's trained (via few-shot prompting and domain examples) to recognize common patterns in Volvo's requirement documents and map them to the internal attribute schema. This eliminates hours of manual reading and transcription while maintaining high accuracy through validation against known schemas.

**Signal Mapping Agent**: Given an attribute definition and access to the CAN signal database, this agent identifies which signals provide the necessary data. This is a complex matching problem—signal names rarely match attribute names directly. A "vehicle speed" attribute might map to signals named `VEH_SPEED_AVG`, `WHEEL_SPEED_FL`, or `GPS_VELOCITY` depending on context and data quality requirements.

The agent uses semantic similarity (via embeddings), pattern matching on signal metadata, and learned heuristics from historical mappings. It proposes candidate signals with confidence scores, which engineers can verify or override. This transforms a tedious database search task into a quick review process.

**Code Generation Agent**: Once the API design and signal mappings are finalized, this agent generates the implementation code. Unlike general code assistants, it works from highly structured inputs—OpenAPI specifications, signal mapping tables, and code generation templates. It fills in templates, generates type-safe accessor functions, implements signal scaling and unit conversions, and produces validation logic.

Because the inputs are structured and the output follows strict patterns, this agent achieves very high accuracy. The generated code is deterministic and auditable, reducing the need for extensive manual review.

**Validation Agent**: This agent generates test cases and validation logic based on attribute constraints and signal specifications. If an attribute has a valid range of 0-100, the agent creates boundary tests. If multiple signals contribute to an attribute, it generates consistency checks. This ensures implementation correctly reflects specification.

### Human-in-the-Loop Validation Points

The workflow automation is not fully autonomous. Strategic human-in-the-loop (HITL) validation points are inserted at key transitions:

- **After Attribute Extraction**: Domain experts review extracted attributes to ensure semantic correctness—the LLM might correctly extract structure but misinterpret domain intent
- **After Signal Mapping**: Engineers verify proposed signal mappings, particularly for safety-critical attributes, using confidence scores to prioritize review
- **Before Code Deployment**: Generated code goes through automated testing and final human audit, especially for security-sensitive endpoints

These HITL points balance automation with safety and quality assurance. They're positioned where domain expertise or safety considerations are paramount, while purely mechanical transformations (like template filling or documentation generation) are fully automated.

The result is a hybrid system combining LLM efficiency with human judgment, achieving both speed and reliability.

### Measuring the Impact

The Volvo Group team conducted rigorous quantitative evaluation across their real production API portfolio:

**Time Reduction**: API development time dropped from an average of 5 hours to under 7 minutes—a 97%+ reduction. This includes the entire workflow from initial attribute definition to generated code ready for integration.

**Quality Metrics**: The automatically generated APIs achieved an F1 score of 93.7% when validated against human expert ground truth. Precision was 95.8% (few false positives—generated APIs rarely included incorrect elements) and recall was 91.7% (few false negatives—generated APIs rarely missed required elements).

**Scale**: The evaluation covered 192 API endpoints, 420 attributes, and 776 CAN signals—representing real production complexity, not toy examples.

**Effort Savings**: Across the entire portfolio, approximately 979 hours of engineering effort were saved. This time was reallocated from mechanical transformation work to higher-value activities like architecture design, performance optimization, and new feature development.

**User Satisfaction**: Domain experts rated the system 4.80/5, appreciating faster turnaround and reduced coordination overhead. Developers rated it 4.67/5, valuing the elimination of tedious mapping tasks and consistent code quality.

These results are remarkable not because LLMs are magical, but because the workflow-first approach ensured automation targeted actual bottlenecks in the development process.

## Key Architectural Patterns: What Made This Work

Several specific architectural decisions were critical to the success of this automation approach. These patterns are generalizable beyond Volvo's context and offer lessons for anyone attempting similar workflow automation.

### 1. Artifact Versioning and Lineage Tracking

Every artifact in the graph is versioned and tracked with full lineage. When a CAN signal definition changes, the system knows exactly which attributes depend on it, which APIs expose those attributes, and which code files need regeneration. This lineage graph enables automated impact analysis and targeted regeneration rather than wholesale rebuilds.

The implementation uses content-addressable storage where each artifact version has a unique hash. Dependencies are tracked as edges between hashes. This creates an immutable audit trail and enables precise incremental updates.

### 2. Declarative Transformation Specifications

Rather than writing imperative code for each transformation, the team defined transformations declaratively. A signal mapping transformation is specified as: "Given attribute schema A and signal database S, produce mapping M such that M satisfies constraints C." The LLM agent satisfies this specification, but the specification itself is separate and version-controlled.

This separation means transformations can be updated, improved, or replaced without changing the workflow graph structure. It also makes transformations testable—you can validate that a transformation satisfies its specification independently of how it's implemented.

### 3. Confidence Scoring and Validation Thresholds

Every LLM-generated output includes confidence scores. These aren't binary "confident/not confident" flags—they're granular scores for specific aspects. For a signal mapping, separate confidence scores might cover semantic similarity (how well does the signal name match the attribute?), data type compatibility, unit consistency, and historical usage patterns.

These scores feed into validation routing. High-confidence outputs proceed automatically to the next stage. Medium-confidence outputs are flagged for quick human review. Low-confidence outputs trigger deeper expert consultation. This adaptive routing optimizes the balance between automation speed and quality assurance.

### 4. Incremental Validation and Fast Feedback

Rather than generating a complete API and validating it as a monolith, the system validates incrementally at each graph node. Attribute definitions are validated against schema constraints immediately. Signal mappings are validated for type safety and unit consistency. Code generation outputs are validated against API design patterns.

This incremental validation provides fast feedback—errors are caught at the earliest possible point, minimizing rework. It also creates a natural structure for parallelization, as independent branches of the graph can be validated concurrently.

### 5. Template Libraries with Domain-Specific Constraints

Code generation relies on template libraries that encode domain-specific constraints and best practices