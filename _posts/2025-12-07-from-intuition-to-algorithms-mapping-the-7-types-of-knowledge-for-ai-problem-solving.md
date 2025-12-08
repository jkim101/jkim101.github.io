---
title: "### **From Intuition to Algorithms - Mapping the 7 Types of Knowledge for AI & Problem Solving**"
date: 2025-12-07 21:55:13 -0500
categories:
  - blog
tags:
  - post
layout: single
author_profile: true
read_time: true
comments: false
share: false
related: true
---

### **From Intuition to Algorithms: Mapping the 7 Types of Knowledge for AI & Problem Solving**

In the age of AI, the challenge for organizations is no longer just "managing data." It is about traversing the DIKW path—turning Data into Information, Knowledge, and ultimately Wisdom. To build truly intelligent systems (like Agentic AI), we must first understand the anatomy of knowledge itself.

Based on the [Helpjuice guide](https://helpjuice.com/blog/types-of-knowledge) and my own engineering perspective, I’ve mapped the **7 Types of Knowledge** into a framework for **Problem Solving** and **Knowledge Representation (KR)**.

#### **1. The 7 Types of Knowledge**

Before we can engineer knowledge, we must classify it:

1. **Tacit:** Internal intuition and "gut feelings" gained from experience.
2. **Explicit:** Documented information (manuals, databases).
3. **Embedded:** Knowledge locked into processes, routines, or code.
4. **Implicit:** "Reading between the lines"—understanding culture and context.
5. **Declarative:** Facts and definitions (What is X?).
6. **Procedural:** Step-by-step guides (How to do X?).
7. **Strategic:** High-level decision-making logic (Why and When?).

------

#### **2. The Problem-Solving Cycle**

How do humans use these knowledge types to solve problems?

- **Step 1: Definition (The "What")**
  - *Knowledge:* **Declarative & Explicit**
  - *Action:* Identifying facts and consulting records. "What is the error code?" "What is the current status?"
- **Step 2: Analysis (The "Why")**
  - *Knowledge:* **Tacit & Implicit**
  - *Action:* Using intuition and context. "This error usually happens when the marketing team runs heavy queries (Context)" or "I feel like it's a memory leak (Intuition)."
- **Step 3: Execution (The "How")**
  - *Knowledge:* **Procedural**
  - *Action:* Following a step-by-step solution. "Run script A, then restart service B."
- **Step 4: Decision (The Strategy)**
  - *Knowledge:* **Strategic**
  - *Action:* Determining the best course of action. "Should we fix it now and risk downtime, or wait until midnight?"
- **Step 5: Systemization (The "Future")**
  - *Knowledge:* **Embedded**
  - *Action:* Hard-coding the solution into the system so it never happens again.

------

#### **3. Engineering View: Knowledge Representation (KR)**

For Data Engineers and AI Architects, the ultimate question is: **"How do we teach this to a machine?"** Here is how we translate human knowledge into AI architecture.

| **Human Knowledge**        | **KR Strategy (AI/Data)**                    | **Implementation Example**                                   |
| -------------------------- | -------------------------------------------- | ------------------------------------------------------------ |
| **Declarative / Explicit** | **Ontology & Knowledge Graph**               | Storing facts as Triples `(Subject, Predicate, Object)` in a Graph DB. |
| **Tacit / Implicit**       | **Vector Embeddings & Probabilistic Models** | Using Vector Search to find semantic similarities or Bayesian Networks to infer causality from patterns. |
| **Procedural**             | **Rules & Planners**                         | IF-THEN logic, DAGs (e.g., Airflow), or PDDL for AI planning agents. |
| **Strategic**              | **Utility & Objective Functions**            | Mathematical formulas that calculate the "Reward" or "Cost" to optimize decisions (Reinforcement Learning). |
| **Embedded**               | **Architecture & Weights**                   | The system code itself, hard constraints, or the frozen weights of a trained Model. |

#### **Conclusion**

Building an "AI Agent" isn't just about feeding text into an LLM. It requires a hybrid architecture. We need **Knowledge Graphs** for facts, **Vectors** for intuition, **Code/Tools** for procedure, and **System Prompts** for strategy.

To solve complex problems, we must ensure our systems possess all seven types of knowledge, not just the ones written in documents.









### **직관에서 알고리즘으로: AI와 문제 해결을 위한 7가지 지식 유형의 설계**

AI 시대에 조직이 직면한 과제는 더 이상 단순한 '데이터 관리'가 아닙니다. DIKW(Data, Information, Knowledge, Wisdom) 모델이 제시하듯, 데이터를 정보로, 지식으로, 그리고 궁극적으로는 지혜로 전환하는 것이 핵심입니다. 진정한 지능형 시스템(Agentic AI)을 구축하기 위해서는 먼저 지식의 구조를 이해해야 합니다.

[Helpjuice의 가이드](https://helpjuice.com/blog/types-of-knowledge)를 바탕으로, **7가지 지식 유형**을 **문제 해결(Problem Solving)** 프로세스와 **지식 표현(Knowledge Representation)**의 관점에서 재구성해 보았습니다.

#### **1. 7가지 지식 유형의 정의**

지식을 엔지니어링하기 위해서는 먼저 분류가 필요합니다.

1. **암묵지 (Tacit):** 경험에서 우러나오는 직관이나 '감(Gut feeling)'.
2. **형식지 (Explicit):** 매뉴얼이나 DB처럼 문서화된 정보.
3. **내재된 지식 (Embedded):** 프로세스, 루틴, 혹은 코드 속에 녹아있는 지식.
4. **묵시적 지식 (Implicit):** 조직 문화나 맥락을 읽어내는 '눈치(Context)'.
5. **선언적 지식 (Declarative):** 사실과 정의에 대한 지식 (What is X?).
6. **절차적 지식 (Procedural):** 단계별 실행 방법 (How to do X?).
7. **전략적 지식 (Strategic):** 의사결정의 이유와 시기 (Why and When?).

------

#### **2. 문제 해결의 관점 (Human Process)**

인간은 문제를 해결할 때 이 지식들을 다음과 같은 순서로 활용합니다.

- **1단계: 정의 (Definition)**
  - *활용 지식:* **선언적 & 형식지**
  - *행동:* 팩트를 확인하고 기록을 대조합니다. "에러 코드가 무엇인가?", "현재 상태는 어떠한가?"
- **2단계: 분석 (Analysis)**
  - *활용 지식:* **암묵지 & 묵시적**
  - *행동:* 직관과 맥락을 사용합니다. "이건 보통 마케팅팀이 쿼리를 돌릴 때 생기는 문제야(맥락)", "메모리 누수 같은데?(직관)"
- **3단계: 실행 (Execution)**
  - *활용 지식:* **절차적**
  - *행동:* 단계별 솔루션을 수행합니다. "스크립트 A를 실행하고, 서비스 B를 재시작한다."
- **4단계: 결정 (Decision)**
  - *활용 지식:* **전략적**
  - *행동:* 최적의 대안을 선택합니다. "지금 고쳐서 다운타임을 감수할까, 아니면 새벽까지 기다릴까?"
- **5단계: 시스템화 (Systemization)**
  - *활용 지식:* **내재된 지식**
  - *행동:* 해결책을 시스템 코드나 프로세스로 고착화하여 재발을 방지합니다.

------

#### **3. 엔지니어링 관점: 지식 표현 (KR)**

데이터 엔지니어와 AI 아키텍트에게 중요한 질문은 **"이 인간의 지식을 기계에게 어떻게 가르칠 것인가?"**입니다.

| **인간의 지식 유형** | **KR 전략 (AI/Data)**           | **구현 기술 예시**                                           |
| -------------------- | ------------------------------- | ------------------------------------------------------------ |
| **선언적 / 형식지**  | **온톨로지 & 지식 그래프**      | 사실(Fact)을 `(주어, 서술어, 목적어)` 형태의 Triple로 Graph DB에 저장. |
| **암묵지 / 묵시적**  | **벡터 임베딩 & 확률 모델**     | 텍스트의 의미를 고차원 벡터로 변환하여 유사도 검색(Vector Search) 수행. |
| **절차적**           | **규칙(Rules) & 플래너**        | IF-THEN 논리, 워크플로우(DAG), 또는 에이전트 도구(Tools) 호출. |
| **전략적**           | **효용 함수(Utility Function)** | 보상(Reward)과 비용(Cost)을 수식화하여 최적의 선택을 계산 (강화학습 등). |
| **내재된 지식**      | **아키텍처 & 가중치**           | 시스템 코드 그 자체, 하드 코딩된 제약 조건, 혹은 학습된 모델의 파라미터(Weights). |

#### **결론**

성공적인 'AI 에이전트'를 만든다는 것은 단순히 LLM에 텍스트를 입력하는 것이 아닙니다. 팩트를 위한 **그래프**, 직관을 위한 **벡터**, 실행을 위한 **코드**, 전략을 위한 **프롬프트**가 결합된 하이브리드 아키텍처가 필요합니다.

복잡한 문제를 해결하는 시스템을 만들기 위해서는 문서에 적힌 지식뿐만 아니라, 보이지 않는 지식까지 시스템에 설계해 넣어야 합니다.