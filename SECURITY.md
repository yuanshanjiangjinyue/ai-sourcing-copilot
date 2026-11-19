# Security notice / 安全说明

This repository is an offline/local proof of concept. The backend exposes draft RFQ creation and listing without authentication. **Do not deploy it on a public server or use real customer/supplier information.**

Before any production pilot, implement authentication and authorization, tenant data isolation, rate limits, abuse prevention, secret storage, logging redaction, retention policy, dependency scanning and human approval for outward-facing commercial actions.

本项目是本地演示，不提供生产级安全保障。请勿公网部署或填入真实客户信息。