---
layout: home
title: Hello AI
description: 大模型全链路工程自学指南

hero:
  name: "Hello AI"
  text: "大模型全链路工程自学指南"
  tagline: 从 Token 和 Transformer 出发，用 ShopLM 贯穿数据、预训练、后训练、对齐、评测、推理部署与线上迭代。
  actions:
    - theme: brand
      text: 开始学习
      link: /guide/01-getting-started
    - theme: alt
      text: 查看学习路线
      link: /roadmap/

features:
  - icon: 🧭
    title: 一条完整路线
    details: 不堆砌零散名词，围绕“为什么、怎么做、如何验证”打通九个工程环节。
  - icon: 🧪
    title: 一个贯穿实验
    details: ShopLM Mini 在普通 CPU 上演示语料、分词、预训练、指令微调、生成和评测。
  - icon: 🏗️
    title: 面向真实工程
    details: 同时理解单机教学实验与生产级分布式训练、服务化和监控之间的映射。
  - icon: 🌱
    title: 开源共建
    details: 教程、代码、路线图和贡献流程全部公开，欢迎通过 Issue 与 Pull Request 参与。
---

## 你最终会获得什么？

完成本项目后，你不只会“调用一个模型”，而是能够解释并动手验证下面这条完整链路：

```mermaid
flowchart LR
  A[目标定义] --> B[数据工程]
  B --> C[Tokenizer]
  C --> D[预训练]
  D --> E[SFT]
  E --> F[偏好与安全对齐]
  F --> G[评测]
  G --> H[推理部署]
  H --> I[监控与数据回流]
  I --> B
```

<div class="learning-path">
  <div><strong>第一阶段 · 看懂</strong><br>建立 Token、注意力、训练目标和推理过程的统一心智模型。</div>
  <div><strong>第二阶段 · 跑通</strong><br>在 CPU 上完成一个小模型从数据到生成的最小闭环。</div>
  <div><strong>第三阶段 · 放大</strong><br>理解小实验如何映射到多 GPU、服务化、安全和持续迭代。</div>
</div>

> [!TIP]
> 如果你只有 Python 基础，从[第 1 章](/guide/01-getting-started)开始；如果已经做过模型调用，可以先阅读[第 3 章](/guide/03-llm-lifecycle)建立全局视角。

## V1 内容状态

| 内容 | 状态 | 产出 |
| --- | --- | --- |
| 学习导览与工程环境 | ✅ 已发布 | 可复现的本地工具链 |
| 大模型核心原理 | ✅ 已发布 | 从 Token 到生成的心智模型 |
| 大模型全链路工程 | ✅ 已发布 | ShopLM 端到端架构方案 |
| ShopLM Mini 实验 | ✅ 已发布 | CPU 可运行的最小训练闭环 |
| 后续专题章节 | 🛠️ Roadmap | 逐章审校后发布 |

下一步：[查看完整课程地图 →](/roadmap/)
