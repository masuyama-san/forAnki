---
type: AnkiCards
title: docker tagでDocker Hubにプッシュするためのタグ付け方法は？
date: 2026-02-08
tags:
  - Docker
  - tag
id: 1753492774658
---

# Card: docker tagでDocker Hubにプッシュするためのタグ付け方法は？

## Question
docker tagでDocker Hubにプッシュするためのタグ付け方法は？

## Answer
docker tag イメージ名 ユーザー名/リポジトリ名:タグ<br><pre><code>docker tag my-app johndoe/my-app:latest        # Docker Hubの個人アカウント用
docker tag webapp company/webapp:v2.0          # Docker Hubの組織アカウント用
docker tag local-image username/public-image:1.0  # バージョン指定でタグ付け</code></pre>
