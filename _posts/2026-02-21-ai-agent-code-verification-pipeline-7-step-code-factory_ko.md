---
title: "AI Agent 코드 검증 자동화: 7단계 Code Factory 파이프라인"
date: 2026-02-21 21:50:05 -0500
categories:
  - blog
tags:
  - AI Agent 코드 검증
  - Code Factory
  - 자동화 파이프라인
  - 코드 리뷰 자동화
  - CI/CD 최적화
  - Policy Gate
  - Review Agent
layout: single
author_profile: true
read_time: true
comments: false
share: false
related: true
---

# AI Agent가 생성한 코드를 검증하는 자동화 파이프라인 구조: 7단계 Code Factory 접근법

오픈클로(OpenClo) 개발자 Peter의 하루 커밋은 3,000회를 넘는 날도 있습니다. AI Agent가 밤새 쌓아놓은 수백 개의 커밋을 아침에 GitHub에서 확인하는 순간, 그는 코드 리뷰의 기본 전제가 완전히 무너졌음을 체감합니다. 하루 8시간 근무를 가정해도 커밋당 10초도 할애할 수 없는 계산입니다. '사람이 코드를 읽고 이해하고 검증한다'는 전통적 방식이 AI Agent 시대에는 물리적으로 불가능해졌습니다.

이런 상황에서 Ryan Carson이 제시한 Code Factory 프레임워크는 근본적인 질문을 던집니다. "사람이 읽는 것을 포기하면 어떻게 될까요?" 그의 답은 명확합니다. 사람이 읽을 수 없다면 기계가 검증할 수 있는 구조를 설계하면 됩니다. Agent가 작성한 코드를 검증하는 주체 역시 기계여야 하고, 기계가 남긴 증거를 기계가 판단하는 자동화 파이프라인을 구축해야 합니다. 이 글에서는 Carson이 제안한 7단계 Code Factory 접근법을 중심으로, AI Agent 시대의 코드 검증 파이프라인을 어떻게 설계해야 하는지 실무 도구와 함께 살펴봅니다.

## 1-2단계: Merge 규칙의 코드화와 Policy Gate로 비용 차단

Code Factory의 첫 번째 단계는 모든 Merge 규칙을 JSON 파일 하나로 선언하는 것입니다. 사람이 매번 "이 경로는 중요하니까 시니어의 승인이 필요해"라고 판단하는 대신, 기계가 읽고 실행할 수 있는 형태로 규칙을 명시합니다.

```json
{
  "paths": {
    "src/payment/**": {
      "risk": "high",
      "required_checks": ["review_agent", "browser_evidence", "integration_test"]
    },
    "src/ui/components/**": {
      "risk": "medium",
      "required_checks": ["review_agent", "visual_regression"]
    },
    "docs/**": {
      "risk": "low",
      "required_checks": ["policy_gate", "ci_build"]
    }
  }
}
```

이런 선언적 구조는 high-risk 경로에는 Review Agent의 승인과 Browser 증거가 필요하고, low-risk 경로는 policy gate와 CI만 통과하면 Merge할 수 있다는 규칙을 명확히 합니다. 더 중요한 것은 문서와 실제 실행 로직의 불일치를 원천적으로 차단한다는 점입니다. 규칙이 코드로 표현되어 있으면 문서 업데이트를 잊어 실제 동작과 문서가 불일치하는 상황이 발생하지 않습니다.

두 번째 단계는 이 규칙을 실제로 집행하는 Policy Gate를 CI 파이프라인의 맨 앞단에 배치하는 것입니다. Carson이 지적하듯 "Review도 끝나지 않은 PR에 Build를 돌리면 돈만 날아갑니다." AI Agent가 생성한 수백 개의 PR이 몰려들 때, 자격 미달인 PR까지 모두 CI 리소스를 소비하게 두는 것은 비효율적입니다.

risk-policy-gate workflow는 PR이 정의된 정책을 충족하는지 먼저 검사합니다.

```yaml
# risk-policy-gate.yml
name: Risk Policy Gate
on: [pull_request]
jobs:
  policy_check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Evaluate merge policy
        run: |
          node scripts/policy-gate.js \
            --pr-files="${{ github.event.pull_request.changed_files }}" \
            --policy-file=".github/merge-policy.json"
      - name: Block if policy violated
        if: failure()
        run: |
          echo "::error::This PR violates merge policy. Required checks missing."
          exit 1
```

Carson이 강조한 핵심 원칙은 "policy gate → Review Agent 확인 → CI fanout 순서 고정"입니다. 이렇게 하면 불필요한 CI 비용을 절감할 뿐 아니라, 개발자나 Agent에게 즉각적인 피드백을 제공해 정책 위반을 조기에 발견할 수 있습니다.

## 3-4단계: Stale Check 무효화와 Rerun Race Condition 방지

세 번째 단계는 낡은 commit 기준의 '통과' 상태를 신뢰하지 않는 구조를 만드는 것입니다. GitHub에서는 PR에 새로운 commit이 push되면 synchronize 이벤트가 발생합니다. 하지만 기존에 실행됐던 check run들은 자동으로 무효화되지 않습니다. Agent가 새 commit을 push했는데 이전 commit 기준으로 통과한 check가 여전히 초록불로 남아 있다면, 실제로는 검증되지 않은 코드가 Merge될 수 있습니다.

Code Factory에서는 Review Check Run이 PR의 head SHA와 정확히 일치할 때만 유효한 것으로 간주합니다. synchronize 이벤트가 발생하면 모든 필수 check를 rerun하도록 강제하여, 최신 코드만 검증을 통과할 수 있게 합니다. 이를 위해 greptile-rerun.yml 같은 canonical rerun workflow를 두고, 이 workflow만 rerun 로직을 담당하게 만듭니다.

네 번째 단계는 rerun 요청의 중복을 방지하는 것입니다. 여러 workflow가 동시에 "이 PR은 rerun이 필요해"라고 판단하면, PR comment가 중복으로 달리고 실제 rerun 요청도 경합 상태에 빠질 수 있습니다. Carson은 이를 해결하기 위해 marker 패턴을 도입했습니다.

```yaml
# greptile-rerun.yml
name: Canonical Rerun Workflow
on:
  pull_request:
    types: [synchronize]
jobs:
  rerun_checks:
    runs-on: ubuntu-latest
    steps:
      - name: Check rerun marker
        id: check_marker
        run: |
          MARKER="rerun-requested:${{ github.event.pull_request.head.sha }}"
          EXISTING=$(gh api repos/${{ github.repository }}/issues/${{ github.event.pull_request.number }}/comments \
            --jq '.[] | select(.body | contains("'"$MARKER"'")) | .id')
          
          if [ -n "$EXISTING" ]; then
            echo "already_requested=true" >> $GITHUB_OUTPUT
          else
            echo "already_requested=false" >> $GITHUB_OUTPUT
          fi
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
      
      - name: Post rerun marker
        if: steps.check_marker.outputs.already_requested == 'false'
        run: |
          gh pr comment ${{ github.event.pull_request.number }} \
            --body "<!-- rerun-requested:${{ github.event.pull_request.head.sha }} --> Triggering check rerun for latest commit."
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
      
      - name: Trigger review agent rerun
        if: steps.check_marker.outputs.already_requested == 'false'
        run: |
          gh workflow run review-agent.yml \
            --ref ${{ github.event.pull_request.head.ref }} \
            -f pr_number=${{ github.event.pull_request.number }} \