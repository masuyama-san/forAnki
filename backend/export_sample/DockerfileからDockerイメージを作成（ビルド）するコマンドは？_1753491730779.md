---
type: AnkiCards
title: DockerfileからDockerイメージを作成（ビルド）するコマンドは？
date: 2026-02-08
tags:
  - build
  - Docker
id: 1753491730779
---

# Card: DockerfileからDockerイメージを作成（ビルド）するコマンドは？

## Question
DockerfileからDockerイメージを作成（ビルド）するコマンドは？

## Answer
docker build<br><pre><code>docker build .                      # 現在ディレクトリのDockerfileからビルド
docker build -t myapp:latest .      # タグ付きでビルド
docker build -f custom.dockerfile . # 特定のDockerfileを指定してビルド</code></pre>
