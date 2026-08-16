# Hello AI：大模型全链路工程自学指南

[![Docs](https://img.shields.io/badge/docs-online-315cfd)](https://jinchengawu.github.io/hello-AI/)
[![CI](https://github.com/Jinchengawu/hello-AI/actions/workflows/ci.yml/badge.svg)](https://github.com/Jinchengawu/hello-AI/actions/workflows/ci.yml)
[![License: CC BY-NC-SA 4.0](https://img.shields.io/badge/content-CC%20BY--NC--SA%204.0-lightgrey.svg)](LICENSE-CONTENT)
[![License: Apache 2.0](https://img.shields.io/badge/code-Apache%202.0-blue.svg)](LICENSE-CODE)

一套面向大模型工程初学者的中文开源教程：从 Token、Transformer 和训练目标出发，用 **ShopLM 电商客服模型**贯穿数据治理、预训练、SFT、偏好对齐、评测、推理部署和线上迭代。

> 在线阅读：<https://jinchengawu.github.io/hello-AI/>

## 为什么做这个项目？

大模型知识经常以论文、框架教程和零散代码存在。Hello AI 希望提供一条可验证的主线：每个阶段不仅解释“是什么”，还说明工程输入、输出、失败模式和验收证据。

## V1 学习路线

| 内容 | 状态 | 主要产出 |
| --- | --- | --- |
| 学习导览与工程环境 | ✅ | 可复现的本地工具链 |
| 大模型核心原理 | ✅ | 从 Token 到生成的心智模型 |
| 大模型全链路工程 | ✅ | ShopLM 端到端系统方案 |
| ShopLM Mini 实验 | ✅ | CPU 可运行的训练闭环 |
| 数据、训练、对齐等专题 | 🛠️ | 按 Roadmap 逐章发布 |

完整路线包含九部分：基础环境、模型原理、数据工程、预训练、后训练、偏好与安全对齐、评测、推理部署、线上迭代。

## 快速开始

文档站要求 Node.js 22 或更高版本：

```bash
git clone git@github.com:Jinchengawu/hello-AI.git
cd hello-AI
npm ci
npm run docs:dev
```

运行 ShopLM Mini（Python 3.11、CPU）：

```bash
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install -r examples/shoplm-mini/requirements.txt
python examples/shoplm-mini/run_pipeline.py --steps 80 --output artifacts/shoplm-mini
```

安装两套依赖后，可执行全部检查：

```bash
PATH="$PWD/.venv/bin:$PATH" npm run check
```

## 仓库结构

```text
docs/                    VitePress 教程与站点配置
examples/shoplm-mini/    CPU 可运行的微型 Decoder 实验
.github/workflows/       构建、检查与 Pages 发布
CONTRIBUTING.md          内容与代码贡献规范
```

## 参与贡献

欢迎修正文档、补充实验、报告问题或参与后续章节。提交前请阅读 [CONTRIBUTING.md](CONTRIBUTING.md) 和 [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)。

## 引用

如果这个项目对你的课程、文章或研究有帮助，可使用仓库中的 [CITATION.cff](CITATION.cff) 引用。

## 许可证

- `docs/`、README 等教程内容采用 [CC BY-NC-SA 4.0](LICENSE-CONTENT)；
- `examples/`、站点配置、脚本和工作流采用 [Apache-2.0](LICENSE-CODE)；
- 第三方依赖与引用资料遵循各自许可证。

Copyright © 2026 Jinchengawu and contributors.
