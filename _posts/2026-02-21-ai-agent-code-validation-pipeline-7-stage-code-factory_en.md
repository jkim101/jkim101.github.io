---
title: "AI Agent Code Validation: 7-Stage Automated Pipeline"
date: 2026-02-21 21:50:05 -0500
categories:
  - blog
tags:
  - AI Agent code validation
  - automated code pipeline
  - Code Factory framework
  - AI-generated code review
  - DevOps automation
  - GitHub Actions workflow
  - policy gate automation
  - visual regression testing
layout: single
author_profile: true
read_time: true
comments: false
share: false
related: true
---

# Automated Pipeline Architecture for Validating AI Agent-Generated Code: A 7-Stage Code Factory Approach

Peter, a developer at OpenClo, sometimes sees over 3,000 commits in a single day. When he checks GitHub each morning to review hundreds of commits accumulated overnight by AI Agents, he realizes the fundamental premise of code review has completely collapsed. Even with an 8-hour workday, the math shows he can't allocate even 10 seconds per commit. The traditional approach of "humans reading, understanding, and validating code" has become physically impossible in the AI Agent era.

The Code Factory framework proposed by Ryan Carson poses a fundamental question: "What if we stop trying to have humans read everything?" His answer is clear: if humans can't read it, we need a structure where machines can validate it. The entity verifying Agent-generated code must also be a machine, requiring an automated pipeline where machines judge evidence left by machines. This article explores how to design a code validation pipeline for the AI Agent era, centered on Carson's 7-stage Code Factory approach, complete with practical tooling.

## Stages 1-2: Codifying Merge Rules and Blocking Costs with Policy Gates

The first Code Factory stage declares all merge rules in a single JSON file. Instead of having humans repeatedly judge "this path is critical so it needs senior approval," we express the rules explicitly in a form machines can read and execute. Consider this JSON structure:

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

This declarative structure makes explicit that high-risk paths require Review Agent approval and browser evidence, while low-risk paths need only policy gate and CI passes. More importantly, it fundamentally prevents divergence between documentation and actual execution logic. When rules exist as code, there's no possibility of stale documentation creating misalignment between documented and actual behavior.

The second stage places a Policy Gate enforcing these rules at the very front of the CI pipeline. As Carson points out, "Running builds on PRs that haven't even passed review just burns money." When hundreds of AI Agent-generated PRs flood in, letting unqualified PRs consume CI resources is wasteful.

The risk-policy-gate workflow first checks whether a PR meets the defined policy:

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

Carson emphasizes a core principle: "fixed order: policy gate → Review Agent verification → CI fanout." This reduces unnecessary CI costs and provides immediate feedback to developers or Agents, enabling early policy violation detection.

## Stages 3-4: Invalidating Stale Checks and Preventing Rerun Race Conditions

The third stage creates a structure that doesn't trust "passing" status from outdated commits. In GitHub, when new commits push to a PR, a synchronize event triggers. However, previously executed check runs don't automatically invalidate. If an Agent pushes new commits while checks that passed for previous commits still show green, unvalidated code could merge.

In Code Factory, a Review Check Run is valid only when it exactly matches the PR's head SHA. When synchronize events occur, all required checks are forced to rerun, ensuring only the latest code passes validation. A canonical rerun workflow like greptile-rerun.yml handles all rerun logic.

The fourth stage prevents duplicate rerun requests. If multiple workflows simultaneously determine "this PR needs a rerun," duplicate PR comments post and actual rerun requests enter race conditions. Carson introduced a marker pattern to solve this:

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
            -f pr_number=${{ github.event.pull_request.number }}
```

This workflow posts a hidden HTML comment containing the head SHA. Other workflows check for this marker before making rerun requests, skipping if it exists. This prevents multiple workflows from competing to trigger reruns and avoids comment spam.

## Stage 5: Making Evidence Machine-Readable with Structured Artifacts

The fifth stage makes validation evidence machine-readable. When an Agent modifies a login form, a Review Agent shouldn't simply comment "I tested the login and it works." That's human-readable but doesn't provide structured evidence another machine can interpret.

Instead, evidence must be structured data. For browser tests:

```json
{
  "test_type": "browser_functional",
  "timestamp": "2024-01-15T03:22:19Z",
  "commit_sha": "abc123def456",
  "test_cases": [
    {
      "name": "user_login_flow",
      "status": "pass",
      "screenshot": "artifacts/login-success.png",
      "console_logs": [],
      "network_requests": 12
    },
    {
      "name": "password_reset_flow",
      "status": "pass",
      "screenshot": "artifacts/reset-success.png"
    }
  ],
  "coverage": {
    "routes_tested": ["/login", "/reset-password"],
    "components_rendered": ["LoginForm", "ResetPasswordForm"]
  }
}
```

This JSON artifact clearly shows which test cases passed, routes tested, and screenshot locations. Other automated processes can parse this artifact to make decisions. A final validation stage can verify whether all policy-declared routes were tested and screenshots exist.

Carson emphasizes the "evidence chain" concept. Each check run must produce artifacts, and subsequent stages consume these artifacts to make decisions. If Review Agent output is unstructured, downstream processes must rely on text parsing or human intervention, reintroducing human bottlenecks. Structured artifacts eliminate this and enable true end-to-end automation.

## Stage 6: Browser Evidence and Visual Regression Detection

The sixth stage addresses validating visual browser changes. When Agents modify UI code, determining whether changes are "correct" is surprisingly difficult. Unit tests might pass while colors are wrong, layouts broken, or buttons invisible.

Code Factory proposes making browser testing a required pipeline step. For high-risk paths (like `/src/ui/`), policies should mandate browser evidence. Review Agents launch real browsers using tools like Playwright or Puppeteer, interact with modified pages, and capture evidence.

```javascript
// browser-evidence-collector.js
const playwright = require('playwright');
const fs = require('fs');

async function collectBrowserEvidence(prNumber, changedFiles) {
  const browser = await playwright.chromium.launch();
  const page = await browser.newPage();
  
  const evidence = {
    pr_number: prNumber,
    timestamp: new Date().toISOString(),
    tests: []
  };
  
  // Identify affected routes
  const affectedRoutes = identifyRoutesFromFiles(changedFiles);
  
  for (const route of affectedRoutes) {
    await page.goto(`http://localhost:3000${route}`);
    
    const screenshotPath = `artifacts/pr-${prNumber}-${route.replace(/\//g, '-')}.png`;
    await page.screenshot({ path: screenshotPath, fullPage: true });
    
    const consoleLogs = [];
    page.on('console', msg => consoleLogs.push(msg.text()));
    
    // Perform basic interactions
    await page.click('button[type="submit"]');
    await page.waitForTimeout(1000);
    
    evidence.tests.push({
      route: route,
      screenshot: screenshotPath,
      console_errors: consoleLogs.filter(log => log.includes('Error')),
      status: consoleLogs.length === 0 ? 'pass' : 'warning'
    });
  }
  
  await browser.close();
  
  fs.writeFileSync(
    `artifacts/browser-evidence-${prNumber}.json`,
    JSON.stringify(evidence, null, 2)
  );
  
  return evidence;
}
```

Advanced pipelines integrate visual regression testing. Tools like Percy, Chromatic, or Playwright's visual comparison take screenshots and compare them pixel-by-pixel with baselines. Differences exceeding thresholds get flagged for human review.

```yaml
# visual-regression.yml
name: Visual Regression Check
on: [pull_request]
jobs:
  visual_test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Install dependencies
        run: npm install
      - name: Run visual regression
        run: npx playwright test --update-snapshots=missing
      - name: Upload visual diff artifacts
        uses: actions/upload-artifact@v3
        with:
          name: visual-diffs
          path: test-results/
```

Incorporating browser evidence and visual regression as required policy checks ensures UI changes don't go unvalidated. This mechanized layer provides confidence that human reviewers no longer need manually verifying every visual change.

## Stage 7: Final Approval Gate and Merge Automation

The seventh and final stage is the approval gate synthesizing all evidence before allowing merge. Even after all checks pass, Code Factory doesn't allow immediate automatic merge. Instead, a final validation step verifies:

1. Are all required artifacts present?
2. Do all check run SHAs match the PR head SHA?
3. Are there unresolved policy violations?
4. Has the required approval threshold been met?

This final gate implements as a merge-gate workflow running on workflow_run completion events or schedule triggers.

```yaml
# merge-gate.yml
name: Final Merge Gate
on:
  workflow_run:
    workflows: ["Risk Policy Gate", "Review Agent", "Visual Regression Check"]
    types: [completed]
jobs:
  evaluate_merge:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Gather all check runs
        id: gather_checks
        run: |
          PR_NUMBER=$(gh pr list --json number,headRefName --jq '.[] | select(.headRefName=="${{ github.ref_name }}") | .number')
          CHECKS=$(gh api repos/${{ github.repository }}/commits/${{ github.sha }}/check-runs --jq '.check_runs')
          echo "checks=$CHECKS" >> $GITHUB_OUTPUT
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
      
      - name: Validate evidence artifacts
        run: |
          node scripts/validate-evidence.js \
            --checks='${{ steps.gather_checks.outputs.checks }}' \
            --required-artifacts='["browser-evidence", "review-summary"]'
      
      - name: Auto-merge if approved
        if: success()
        run: |
          gh pr merge $PR_NUMBER --auto --squash
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

Carson's key insight: "the final gate is not about preventing bad merges—it's about ensuring we have enough evidence to make a confident decision." All previous stages have validated the code; this gate confirms the validation process itself executed properly.

For low-risk paths, the final gate might automatically approve and merge. For high-risk paths, it might post a summary comment requesting human approval, but even then humans review synthesized evidence rather than raw code. They check whether the Review Agent tested the right scenarios, browser evidence looks reasonable, and visual diffs are acceptable—not whether every line of code is correct.

## Practical Implementation: Workflow Integration Pattern

Implementing the 7-stage Code Factory requires careful workflow orchestration. Here's a complete integration pattern:

```yaml
# code-factory-orchestrator.yml
name: Code Factory Orchestrator
on:
  pull_request:
    types: [opened, synchronize, reopened]

jobs:
  stage1_policy_check:
    runs-on: ubuntu-latest
    outputs:
      risk_level: ${{ steps.evaluate.outputs.risk }}
      required_checks: ${{ steps.evaluate.outputs.checks }}
    steps:
      - uses: actions/checkout@v3
      - name: Evaluate merge policy
        id: evaluate
        run: |
          RESULT=$(node scripts/policy-gate.js \
            --pr-files="$(gh pr view ${{ github.event.pull_request.number }} --json files --jq '.files[].path')" \
            --policy-file=".github/merge-policy.json")
          echo "risk=$(echo $RESULT | jq -r '.risk')" >> $GITHUB_OUTPUT
          echo "checks=$(echo $RESULT | jq -c '.required_checks')" >> $GITHUB_OUTPUT
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}

  stage2_stale_check:
    needs: stage1_policy_check
    runs-on: ubuntu-latest
    steps:
      - name: Invalidate stale checks
        run: |
          CURRENT_SHA="${{ github.event.pull_request.head.sha }}"
          STALE_RUNS=$(gh api repos/${{ github.repository }}/commits/$CURRENT_SHA/check-runs \
            --jq '.check_runs[] | select(.status=="completed" and .head_sha!="'"$CURRENT_SHA"'") | .id')
          
          for RUN_ID in $STALE_RUNS; do
            echo "Invalidating check run $RUN_ID"
            # Mark as stale in database or trigger rerun
          done
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}

  stage3_review_agent:
    needs: [stage1_policy_check, stage2_stale_check]
    if: contains(fromJSON(needs.stage1_policy_check.outputs.required_checks), 'review_agent')
    uses: ./.github/workflows/review-agent.yml
```