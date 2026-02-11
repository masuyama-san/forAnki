---
type: AnkiCards
title: Docker Hubや他のレジストリからDockerイメージをダウンロードするコマンドは？
date: 2026-02-08
tags:
  - Docker
  - pull
id: 1753164949645
---

# Card: Docker Hubや他のレジストリからDockerイメージをダウンロードするコマンドは？

## Question
Docker Hubや他のレジストリからDockerイメージをダウンロードするコマンドは？

## Answer
docker pull イメージ名<br><pre><code>docker pull nginx              # 最新のnginxイメージをダウンロード
docker pull ubuntu:20.04       # Ubuntu 20.04の特定バージョンをダウンロード
docker pull mysql:latest       # 最新のMySQLイメージをダウンロード</code></pre>
