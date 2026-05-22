# 🚀 Scaled FinTech Hub & Subscription Manager Backend

<p align="center">
  <img src="https://img.shields.io/badge/Database-MySQL%208.0-blue?style=for-the-badge&logo=mysql&logoColor=white" alt="MySQL" />
  <img src="https://img.shields.io/badge/Language-Python%203-darkgreen?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/Environment-macOS-lightgrey?style=for-the-badge&logo=apple&logoColor=white" alt="macOS" />
  <img src="https://img.shields.io/badge/Security-Protected-red?style=for-the-badge&logo=dependabot&logoColor=white" alt="Security" />
</p>

---

## 📋 Project Overview

A robust, enterprise-grade relational database architecture integrated seamlessly with an interactive Python Command-Line Interface (CLI). This platform simulates a production-ready financial ecosystem, tracking everyday multi-category expenses alongside continuous, multi-tier recurring digital subscription plans.

### ⭐ Core Design Capabilities
* 🛡️ **SQL Injection Protection:** Complete security boundary implementation using strictly parameterized backend queries.
* 🔗 **Referential Integrity Guardrails:** Automated system maintenance leveraging `ON DELETE CASCADE` mappings across critical entity junctions.
* 📐 **Enterprise Data Normalization:** Structural separation dividing user metadata, general ledger items, merchant catalogs, and distinct subscription configurations.

---

## 📐 Relational Architecture & ER Diagram

The backend pipeline scales transactional processing through structural, multi-table mappings:
* **One-to-Many ($1:N$):** A single master profile tracks structural, itemized expenditure timelines.
* **Many-to-Many ($M:N$):** Dynamic marketplace plans map concurrently to overlapping profile portfolios through an automated junction ledger.

```mermaid
erDiagram
    USERS ||--o{ TRANSACTIONS : "logs (1:N)"
    USERS ||--o{ USER_SUBSCRIPTIONS : "enrolls (1:N)"
    MERCHANTS ||--o{ SUBSCRIPTIONS : "provisions (1:N)"
    SUBSCRIPTIONS ||--o{ USER_SUBSCRIPTIONS : "tracks (1:N)"

    USERS {
        int user_id PK
        string username
        string email
        timestamp created_at
    }
    TRANSACTIONS {
        int transaction_id PK
        int user_id FK
        decimal amount
        string category
        date transaction_date
    }
    MERCHANTS {
        int merchant_id PK
        string name
        string category
        string support_email
    }
    SUBSCRIPTIONS {
        int subscription_id PK
        int merchant_id FK
        string plan_name
        enum billing_cycle
        decimal cost
    }
    USER_SUBSCRIPTIONS {
        int user_id PK, FK
        int subscription_id PK, FK
        date start_date
        date next_billing_date
        enum status
    }


Layer,Component,Description
Database Engine,MySQL Community Server,Local high-performance relation engine handling indices and data persistence.
Runtime Language,Python 3.x,Controls frontend option validation and business logic calculations.
Database Connector,mysql-connector-python,Driver processing relational pipelines securely on Mac architecture.
Configuration Security,python-dotenv,Decouples local server login keys into un-tracked local workspaces.
