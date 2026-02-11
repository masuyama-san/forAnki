---
type: AnkiCards
title: FROM命令は必ずDockerfileのどこに記述する必要がある？
date: 2026-02-08
tags:
  - Docker
  - Dockerfile
  - FROM
id: 1753493838008
---

# Card: FROM命令は必ずDockerfileのどこに記述する必要がある？

## Question
FROM命令は必ずDockerfileのどこに記述する必要がある？

## Answer
最初（他のすべての命令より前）<br><pre><code># 正しい例
FROM python:3.9
WORKDIR /app
COPY . .

# 間違った例（FROMが最初でない）
# WORKDIR /app  ← エラーになる
# FROM python:3.9</code></pre>
