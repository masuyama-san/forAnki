---
type: AnkiCards
title: docker buildで特定のDockerfileを指定するオプションは？
date: 2026-02-08
tags:
  - build
  - Docker
id: 1753491993753
---

# Card: docker buildで特定のDockerfileを指定するオプションは？

## Question
docker buildで特定のDockerfileを指定するオプションは？

## Answer
docker build -f Dockerfile名<br><code>-f </code>:&nbsp;"file"（ファイル）<br><pre><code>docker build -f Dockerfile.prod .   # 本番用Dockerfileを指定
docker build -f docker/Dockerfile . # サブディレクトリのDockerfileを指定
docker build -f dev.dockerfile -t myapp:dev .  # 開発用設定でビルド</code></pre>
