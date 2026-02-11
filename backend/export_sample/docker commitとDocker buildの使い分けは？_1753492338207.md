---
type: AnkiCards
title: docker commitとDocker buildの使い分けは？
date: 2026-02-08
tags:
  - build
  - commit
  - Docker
id: 1753492338207
---

# Card: docker commitとDocker buildの使い分けは？

## Question
docker commitとDocker buildの使い分けは？

## Answer
docker commit：既存コンテナの状態保存
<br>docker build：Dockerfileからの再現可能なビルド<br><pre><code># docker commit: 手動設定した環境の保存
docker commit configured-container my-custom-image

# docker build: 再現可能な自動化されたビルド
docker build -t my-app:latest .</code></pre>
