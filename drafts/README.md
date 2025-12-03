# 📝 Blog Post Drafts

이 폴더에 마크다운 파일을 작성하고 `publish_post.py` 스크립트로 자동 발행할 수 있습니다.

## 사용 방법

### 1. 초안 작성
`drafts/` 폴더에 마크다운 파일을 작성합니다.

**예시: `drafts/my-awesome-post.md`**
```markdown
# 나의 멋진 블로그 글

이것은 첫 번째 단락입니다.

## 소제목

내용을 자유롭게 작성하세요!
```

### 2. 발행하기

#### 방법 1: Python 스크립트 사용
```bash
python3 publish_post.py drafts/my-awesome-post.md
```

#### 방법 2: Shell 스크립트 사용 (더 간단!)
```bash
./publish.sh drafts/my-awesome-post.md
```

### 3. 자동 처리되는 내용

스크립트가 자동으로:
- ✅ 제목 추출 (첫 번째 `#` 헤딩 또는 첫 줄)
- ✅ YAML front matter 추가
- ✅ 파일명을 Jekyll 형식으로 변경 (`YYYY-MM-DD-제목.md`)
- ✅ `docs/_posts/`로 이동
- ✅ Git에 커밋
- ✅ GitHub로 푸시 (확인 후)

### 4. 이미 YAML front matter가 있는 경우

이미 front matter가 있는 마크다운 파일도 그대로 사용 가능합니다!

```markdown
---
title: "내 제목"
categories:
  - tech
tags:
  - coding
---

본문 내용...
```

## 기본 설정

스크립트가 자동으로 추가하는 YAML front matter:
- `title`: 자동 추출
- `date`: 현재 시간
- `categories`: blog
- `tags`: post
- `layout`: single
- `author_profile`: true
- `read_time`: true
- `comments`: true
- `share`: true
- `related`: true

## 고급 사용법

### Git 커밋 없이 파일만 생성
```bash
python3 publish_post.py drafts/my-post.md --no-commit
```

## 팁

- 초안 파일명은 자유롭게 작성 가능 (자동으로 Jekyll 형식으로 변환됨)
- 제목에 한글, 영어, 특수문자 모두 사용 가능
- 첫 번째 `#` 헤딩이 제목으로 사용되므로 반드시 포함하세요
