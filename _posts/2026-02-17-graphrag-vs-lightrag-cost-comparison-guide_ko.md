---
title: "GraphRAG vs LightRAG 비용 비교: 6,000배 토큰 절감 RAG 선택 가이드"
date: 2026-02-17 20:18:38 -0500
categories:
  - blog
tags:
  - GraphRAG vs LightRAG
  - RAG 비용 최적화
  - 지식 그래프 검색
  - LLM 애플리케이션 비용
  - 듀얼 레벨 검색
  - GraphRAG 비용
  - LightRAG 토큰 절감
  - RAG 시스템 선택
layout: single
author_profile: true
read_time: true
comments: false
share: false
related: true
---

# GraphRAG vs LightRAG: Cost-Efficient Knowledge Graph Retrieval for LLM Applications

## Introduction: The $400 Wake-Up Call — Why RAG Costs Matter

지난달, 5만 개의 문서로 GraphRAG를 테스트하다가 하루 만에 400달러가 날아갔습니다. 쿼리 한 번에 61만 개의 토큰을 소비하는 줄 미처 몰랐죠. API 호출 비용이 눈덩이처럼 불어나는 걸 보면서 든 생각은 하나였습니다. "이건 지속 가능하지 않다."

전통적인 RAG(Retrieval-Augmented Generation) 시스템의 문제는 간단합니다. 문서를 독립적인 청크로 나눠서 벡터 유사도로만 검색하다 보니, **엔티티 간의 관계가 완전히 사라집니다**. 예를 들어볼까요?

"우리 CEO가 투자한 벤처 중에서 지속가능성 이니셔티브와 연결된 건 뭐가 있지?"

이런 질문에 답하려면 단순한 키워드 매칭이 아니라, CEO → 투자 → 벤처 → 지속가능성이라는 **관계의 체인**을 이해해야 합니다. 바로 여기서 지식 그래프 기반 RAG가 필요합니다.

하지만 강력한 성능에는 비용이 따라옵니다. 2024년 10월, 홍콩대학교 연구팀이 던진 질문은 명확했습니다. "대부분의 이점은 유지하면서 비용을 6,000분의 1로 줄일 수 있다면?"

## GraphRAG: Deep Relational Understanding at a Premium Price

GraphRAG는 2024년 4월 Microsoft Research에서 발표한 시스템입니다. 핵심 아이디어는 문서에서 지식 그래프를 구축하고, **커뮤니티 탐지**를 통해 계층적 요약을 만드는 것입니다.

### 5단계 파이프라인

GraphRAG는 다음 과정을 거쳐 작동합니다.

1. **문서 청크 분할**: 긴 문서를 처리 가능한 단위로 나눕니다
2. **엔티티/관계 추출**: LLM을 사용해 각 청크에서 엔티티와 그들의 관계를 추출합니다
3. **Leiden 알고리즘 클러스터링**: 관련된 엔티티들을 커뮤니티로 그룹화합니다
4. **커뮤니티 요약 생성**: 각 커뮤니티에 대한 계층적 요약을 만듭니다
5. **쿼리 실행**: Global 또는 Local 검색 모드로 질의합니다

### Global vs Local Search

**Global Search**는 전체 커뮤니티 요약을 활용한 map-reduce 방식입니다. "우리 산업의 주요 트렌드는 뭐지?"처럼 큰 그림을 보는 질문에 강합니다.

**Local Search**는 특정 엔티티에서 시작해서 이웃 노드로 확장하는 방식입니다. "이 특정 제품의 공급망은 어떻게 구성되어 있지?"같은 구체적인 질문에 적합합니다.

### 문제는 비용입니다

GraphRAG의 성능은 인상적이지만, 쿼리 한 번에 약 **61만 개의 토큰**과 수백 번의 API 호출이 필요합니다. 5만 개 문서 규모에서 하루에 400달러가 나가는 건 우연이 아닙니다.

```python
# GraphRAG 쿼리 예시 (의사코드)
graph = GraphRAG(documents)
result = graph.global_search("주요 트렌드는?")
# 내부적으로:
# - 모든 커뮤니티 요약 로드 (수백 개)
# - 각 요약에 대해 LLM 호출 (map)
# - 결과 통합 (reduce)
# 총 토큰: ~610,000
```

## LightRAG: 6,000x Fewer Tokens with Dual-Level Retrieval

2024년 10월, 홍콩대학교 연구팀이 LightRAG를 발표했습니다. 핵심 질문은 간단했습니다. "비싼 커뮤니티 클러스터링 단계를 완전히 건너뛰면 어떻게 될까?"

### 4단계 파이프라인

LightRAG는 더 간결한 접근 방식을 취합니다.

1. **엔티티/관계 추출**: GraphRAG와 동일하게 시작합니다
2. **듀얼 레벨 키-밸류 페어 생성**: 여기가 핵심입니다
3. **벡터 기반 검색**: 전통적인 벡터 검색을 활용합니다
4. **LLM 응답 생성**: 단일 API 호출로 답변을 생성합니다

### 비밀 병기: 듀얼 레벨 검색

LightRAG의 진짜 혁신은 **듀얼 레벨 검색**입니다.

- **Low-level**: 정확한 엔티티와 직접 관계를 찾습니다
- **High-level**: 더 넓은 맥락으로 확장된 연결을 찾습니다

이 두 레벨이 **병렬로 실행**되면서, 커뮤니티 탐지 없이도 관계적 맥락을 포착합니다.

```python
# LightRAG 쿼리 예시 (의사코드)
light_rag = LightRAG(documents)
result = light_rag.query("CEO 투자와 지속가능성 연결은?")
# 내부적으로:
# 1. 쿼리를 임베딩으로 변환
# 2. Low-level: "CEO" + "투자" 직접 관계 검색
# 3. High-level: 확장된 맥락 검색 (지속가능성)
# 4. 단일 LLM 호출로 답변 생성
# 총 토큰: ~100
```

### 중요한 주의사항

6,000배 토큰 절감은 **쿼리 단계에만** 적용됩니다. 인덱싱 비용은 두 시스템 모두 비슷합니다. 두 시스템 모두 엔티티와 관계를 추출하기 위해 LLM을 호출해야 하기 때문입니다.

하지만 쿼리는 반복적으로 실행됩니다. 인덱싱은 한 번만 하지만, 쿼리는 하루에 수백, 수천 번 실행될 수 있습니다. 여기서 비용 차이가 극적으로 벌어집니다.

## Head-to-Head Comparison: Performance, Cost, and Practical Trade-offs

### 비용 비교

| 항목 | GraphRAG | LightRAG |
|------|----------|----------|
| 쿼리당 토큰 | ~610,000 | ~100 |
| API 호출 | 수백 번 | 1번 |
| 인덱싱 비용 | 높음 | 높음 (비슷함) |

하루에 100번의 쿼리를 실행한다면:
- GraphRAG: 6,100만 토큰 ≈ $122 (GPT-4 기준)
- LightRAG: 10,000 토큰 ≈ $0.02

**한 달이면 $3,660 vs $0.60**입니다. 스타트업이 지속 가능한 제품을 만들 수 있는지 없는지를 가르는 차이입니다.

### 성능 비교

실제 사용에서 두 시스템은 명확한 차이를 보입니다.

- **속도**: LightRAG가 약 30% 더 빠릅니다 (단일 API 호출의 위력)
- **정확도**: 대부분의 쿼리에서 비슷하지만, GraphRAG가 복잡한 다중 홉 추론에서는 약간 우세합니다
- **업데이트**: LightRAG는 append-only 방식으로 쉽게 증분 업데이트 가능합니다. GraphRAG는 전체 재구축이 필요합니다

### LightRAG의 한계

1. **신기술 리스크**: 2024년 10월 출시로 리소스와 통합 사례가 적습니다
2. **커뮤니티 탐지 불가**: 큰 그림의 테마 분석이 필요하면 GraphRAG가 유리합니다
3. **복잡한 다중 홉 관계**: A → B → C → D 같은 긴 추론 체인에서는 GraphRAG가 더 안정적입니다

### LightRAG의 강점

1. **비용 효율성**: 쿼리 단계에서 ~99.98% 비용 절감
2. **간단한 아키텍처**: 유지보수가 쉽고 디버깅이 명확합니다
3. **빠른 응답**: 실시간 애플리케이션에 적합합니다
4. **동적 데이터**: 자주 변하는 데이터에 이상적입니다

## Decision Framework: When to Choose GraphRAG vs LightRAG

### GraphRAG를 선택해야 할 때

✅ **예산에 여유가 있을 때**: 쿼리당 비용이 문제가 되지 않는 경우  
✅ **정적 데이터**: 자주 업데이트되지 않는 지식베이스  
✅ **글로벌 테마 쿼리**: "우리 산업의 주요 트렌드는?" 같은 질문이 많을 때  
✅ **커뮤니티 인사이트**: 엔티티 클러스터 간의 관계를 이해해야 할 때  

### LightRAG를 선택해야 할 때

✅ **비용에 민감한 프로젝트**: 스타트업, MVP, 제한된 예산  
✅ **자주 변하는 데이터**: 뉴스, 실시간 업데이트, 동적 콘텐츠  
✅ **빠른 응답 필요**: 챗봇, 고객 지원, 실시간 분석  
✅ **간단한 아키텍처 선호**: 작은 팀, 빠른 배포가 중요할 때  

### 빠른 참고 가이드

```
질문 체크리스트:

1. 하루 쿼리 수가 100개 이상인가?
   → YES: LightRAG 강력 추천

2. 커뮤니티 레벨 분석이 핵심인가?
   → YES: GraphRAG 필요

3. 데이터가 주간 단위로 업데이트되는가?
   → YES: LightRAG 유리

4. 예산이 월 $100 미만인가?
   → YES: LightRAG 거의 필수

5. 복잡한 3-hop 이상 추론이 빈번한가?
   → YES: GraphRAG 고려
```

## 결론: Start with LightRAG, Upgrade When Proven Necessary

GraphRAG와 LightRAG는 경쟁 관계가 아닙니다. 각자의 강점이 있는 다른 도구입니다. GraphRAG는 깊이 있는 관계 이해가 필요한 대규모 조직에 적합하고, LightRAG는 비용 효율적인 솔루션이 필요한 스타트업과 MVP에 이상적입니다.

제 경험에서 배운 교훈은 명확합니다. **먼저 LightRAG로 시작하세요.** 대부분의 경우 충분합니다. 그리고 정말로 커뮤니티 탐지나 글로벌 테마 분석이 필요하다는 걸 증명할 수 있을 때만 GraphRAG로 전환하세요.

6,000배의 토큰 차이는 숫자 놀이가 아닙니다. 지속 가능한 제품과 파산 사이의 차이입니다. 현명하게 선택하세요.

```python
# 시작하기 좋은 간단한 의사 결정 코드
def choose_rag_system(
    daily_queries: int,
    budget_per_month: float,
    data_update_frequency: str,
    need_community_detection: bool
):
    if budget_per_month < 100 or daily_queries > 100:
        return "LightRAG"
    
    if need_community_detection and data_update_frequency == "rarely":
        return "GraphRAG"
    
    if data_update_frequency in ["daily", "weekly"]:
        return "LightRAG"
    
    return "LightRAG"  # 의심스러울 때는 비용 효율적인 쪽으로

# 당신의 프로젝트는?
recommendation = choose_rag_system(
    daily_queries=150,
    budget_per_month=50,
    data_update_frequency="weekly",
    need_community_detection=False
)
print(f"추천 시스템: {recommendation}")
```