# AI Sourcing Copilot — 工业品智能选型与询价原型

**A runnable, local-first proof of concept — not a deployed AI purchasing service.**  
**可运行的本地概念验证项目；不是已上线的 AI 采购平台。**

> ⚠️ Product data is **100% synthetic** (16 illustrative SKUs). No LLM, embeddings, vector DB, live supplier data, quotes, payments or real purchase orders are connected. The backend has no authentication and **must not be exposed publicly**.
>
> ⚠️ 全部商品数据均为虚构样例；规则解析非大模型，尚未接入真实供应商、库存和报价。FastAPI 后端无身份认证，请勿直接暴露到公网。

## Try the demo / 一键运行

**Static offline demo:** open [`AI采购选型_在线演示单文件.html`](AI采购选型_在线演示单文件.html) in a modern browser. No setup needed.  
**离线演示：** 下载并双击上述 HTML 文件。

**Backend/API (Python 3.11+):**

```bash
python -m pip install -r requirements.txt
uvicorn app.main:app --host 127.0.0.1 --port 8000
```

Open `http://127.0.0.1:8000` for the UI, `http://127.0.0.1:8000/docs` for the OpenAPI explorer.

**Run tests:**

```bash
python -m pip install -r requirements-dev.txt
python -m unittest discover -s tests -v
```

## What it does / 当前能力

- Natural-language requirement parsing with simple **rules/regex**; not an LLM / 基于规则的需求解析
- Editable hard constraints: interface, shutter, OS, architecture, megapixels, FPS, unit-price cap / 可编辑硬约束
- Explainable matching: **eligible**, **manual review**, **rejected** / 合格、待核实、拒绝及原因
- Compare products and create **draft RFQs only** / 商品对比、仅生成 RFQ 草稿
- FastAPI endpoints plus local SQLite storage / API 与本地草稿存储

The matching engine labels unverified compatibility as **needs_review** and rejects known conflicts. The standalone browser UI and backend API use separate synthetic demonstration catalogs. A semantic retrieval service, PostgreSQL + pgvector and an LLM requirement-extraction adapter are **proposed architecture**, not implemented components.

## Project files / 文件说明

| Path | Purpose |
| --- | --- |
| `AI采购选型_在线演示单文件.html` | Self-contained browser prototype (HTML/CSS/JS) |
| `app/` | FastAPI endpoints, matching and synthetic catalog (API and static demo are independent) |
| `tests/` | Regression tests |
| `docs/04_验收与下一版清单.md` | Product requirements checklist and next milestones |
| `docs/02_系统技术架构.md` | Planned technical architecture |
| `docs/schema.sql` | Proposed future PostgreSQL schema (not deployed) |
| `docs/03_OpenAPI_接口定义.json` | Demo API description |
| `docs/` | Proposed architecture, OpenAPI contract, SQL schema and acceptance plan |

## Security / 安全

This is a **demo**. No login, access control, rate limiting, secret management, production security review or tenant isolation. Never import real customer / supplier data without permission, and do not expose RFQ endpoints to the internet. See [SECURITY.md](SECURITY.md).

## Intellectual property / 使用与授权

**No open-source license is granted in this repository at this time.** Publicly viewable code does not automatically mean permission to copy, modify, distribute or use commercially. Contact the repository owner for licensing. Third-party names and trademarks remain with their owners. This repository is a demonstration, not a claim of patentability or patent ownership.

> 发布源码可能影响后续专利新颖性。此公开版本不包含客户名单、内部报价策略、未公开技术交底或商业秘密。