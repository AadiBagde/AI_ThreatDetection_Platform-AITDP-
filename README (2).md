<div align="center">

# 🛡️ AITDP
### AI-Powered Intelligent Threat Detection Platform

*A modular, distributed AI cybersecurity platform — engineered for modern SOC & SIEM environments*

---

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![React](https://img.shields.io/badge/React-18+-61DAFB?style=for-the-badge&logo=react&logoColor=black)
![TypeScript](https://img.shields.io/badge/TypeScript-5+-3178C6?style=for-the-badge&logo=typescript&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-ML-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=for-the-badge&logo=docker&logoColor=white)

![Status](https://img.shields.io/badge/Status-Active%20Development-brightgreen?style=flat-square)
![Phase](https://img.shields.io/badge/Phase-4%20of%2011-blue?style=flat-square)
![Architecture](https://img.shields.io/badge/Architecture-Microservices-orange?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

</div>

---

## 📌 Overview

**AITDP** is a production-inspired, microservice-based AI cybersecurity platform that simulates the backend intelligence pipeline of modern Security Operations Center (SOC) tooling, SIEM systems, and AI-powered threat detection engines.

The platform ingests raw network packets, extracts ML-ready features, classifies threats using a trained Random Forest model, assigns confidence scores and severity levels, and surfaces live analytics through a SOC-style React dashboard — all across independently scalable microservices.

> AITDP is engineered to mirror the architecture patterns found in enterprise cybersecurity platforms such as Splunk, Darktrace, and CrowdStrike — built from first principles using Python, FastAPI, and modern ML tooling.

---

## ✨ Platform Highlights

| Capability | Details |
|---|---|
| 🔬 **ML Threat Classification** | Random Forest model classifying 5 threat categories |
| 📊 **Confidence Scoring** | Per-prediction confidence with probability distributions |
| ⚡ **Severity Engine** | Automated low / medium / high severity routing |
| 🔗 **Microservice Architecture** | Fully decoupled ingestion, feature, and ML services |
| 🧠 **Feature Engineering** | Protocol encoding, IP analysis, risk scoring, normalization |
| 📡 **REST API Pipeline** | Validated, schema-enforced API contracts across all services |
| 🖥️ **SOC Dashboard** | Live React dashboard with charts, health monitors, packet explorer |
| 🧪 **Test Coverage** | Unit, API, integration, and end-to-end pipeline tests |

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    CLIENT / SOC DASHBOARD                       │
│                 React + TypeScript + Recharts                   │
└─────────────────────────┬───────────────────────────────────────┘
                          │  HTTP / REST
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│               INGESTION SERVICE  :8000                          │
│   • Schema validation    • Request logging                      │
│   • Packet sanitization  • Temporary storage                    │
│   POST /ingest           GET /health                            │
└─────────────────────────┬───────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│               FEATURE ENGINE  :8001                             │
│   • Protocol encoding    • IP classification                    │
│   • Traffic analysis     • Risk scoring                         │
│   • Feature normalization                                       │
│   POST /extract          GET /health                            │
└─────────────────────────┬───────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│               ML ENGINE  :8002                                  │
│   • Random Forest inference  • Confidence scoring               │
│   • Severity classification  • Threat labeling                  │
│   POST /predict              GET /health                        │
└─────────────────────────┬───────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│           THREAT PREDICTION & ANALYTICS OUTPUT                  │
│   label | confidence | severity | features | metadata           │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📂 Project Structure

```
aitdp/
├── ingestion_service/          # Packet ingestion microservice
│   ├── main.py                 # FastAPI app entry point
│   ├── routes/
│   │   └── ingest.py           # POST /ingest endpoint
│   ├── models/
│   │   └── packet.py           # Pydantic packet schema
│   ├── validators/
│   │   └── packet_validator.py # Schema & payload validation
│   └── utils/
│       └── logger.py           # Structured request logging
│
├── feature_engine/             # Feature extraction microservice
│   ├── main.py
│   ├── routes/
│   │   └── extract.py          # POST /extract endpoint
│   ├── extractors/
│   │   ├── protocol.py         # Protocol encoding
│   │   ├── ip_analysis.py      # Private/public IP classification
│   │   ├── port_analysis.py    # Port categorization
│   │   ├── traffic.py          # Traffic pattern analysis
│   │   └── risk_scorer.py      # Risk scoring engine
│   └── utils/
│       └── normalizer.py       # Feature normalization
│
├── ml_engine/                  # ML inference microservice
│   ├── main.py
│   ├── routes/
│   │   └── predict.py          # POST /predict endpoint
│   ├── inference/
│   │   ├── model_loader.py     # Model loading & caching
│   │   ├── predictor.py        # Inference pipeline
│   │   └── confidence.py       # Confidence scoring
│   └── classifiers/
│       └── severity.py         # Severity mapping engine
│
├── shared/                     # Shared utilities & schemas
│   ├── schemas.py              # Shared Pydantic models
│   ├── exceptions.py           # Custom exception handlers
│   └── config.py               # Environment configuration
│
├── models/                     # Trained ML artifacts
│   ├── random_forest.pkl       # Serialized classifier
│   ├── scaler.pkl              # Feature scaler
│   └── metadata.json           # Model metadata & version info
│
├── dashboard/                  # SOC Frontend (React + TypeScript)
│   ├── src/
│   │   ├── components/
│   │   │   ├── ThreatFeed.tsx
│   │   │   ├── SeverityChart.tsx
│   │   │   ├── HealthMonitor.tsx
│   │   │   └── PacketExplorer.tsx
│   │   ├── pages/
│   │   ├── hooks/
│   │   └── api/
│   ├── package.json
│   └── vite.config.ts
│
├── training/                   # ML training pipeline
│   ├── preprocess.py
│   ├── train.py
│   └── evaluate.py
│
├── tests/                      # Test suite
│   ├── unit/
│   ├── api/
│   ├── integration/
│   └── e2e/
│       └── test_pipeline.py    # Full packet → prediction tests
│
└── scripts/                    # Utility scripts
    ├── start_services.sh
    └── smoke_test.sh
```

---

## 🧠 ML & AI Workflow

The AITDP intelligence pipeline follows a structured, stage-gated inference flow:

```
Raw Packet (JSON)
       │
       ▼
[ Ingestion Service ]
  Schema validation
  Payload sanitization
       │
       ▼
[ Feature Engine ]
  Protocol encoding (TCP=0, UDP=1, ICMP=2 ...)
  Source / destination port categorization
  Private / public IP classification
  Connection direction inference
  Suspicious pattern detection
  Risk scoring (0.0 – 1.0)
  Feature vector normalization
       │
       ▼
[ ML Engine ]
  Load Random Forest classifier (cached)
  Apply preprocessing pipeline (scaler)
  Run inference → class probabilities
  Select predicted threat label
  Calculate confidence score
  Map to severity level
       │
       ▼
Structured Prediction Response
  { label, confidence, severity, probabilities, metadata }
```

**Threat Classes:** `benign` · `dos` · `port_scan` · `brute_force` · `suspicious`

**Severity Levels:** `low` · `medium` · `high`

---

## 🖥️ Dashboard

The Phase 4 frontend delivers a SOC-style monitoring interface built with React, TypeScript, and TailwindCSS.

> 📸 *Dashboard screenshots — coming with Phase 4 release*

```
┌───────────────────────────────────────────────────────┐
│  AITDP  SOC Dashboard                    ● LIVE       │
├──────────────┬────────────────┬──────────────────────-┤
│ Threat Feed  │ Severity Chart │ System Health          │
│              │                │ Ingestion  ● OK        │
│ [HIGH] DoS   │  ████ High     │ Features   ● OK        │
│ [MED]  Scan  │  ███  Medium   │ ML Engine  ● OK        │
│ [LOW]  Benign│  █    Low      │                        │
├──────────────┴────────────────┴────────────────────────┤
│ Packet Explorer — Raw → Features → Prediction          │
└───────────────────────────────────────────────────────┘
```

**Dashboard Panels:**
- **Threat Feed** — Live stream of classified threats with confidence and severity
- **Severity Distribution** — Real-time chart of threat severity breakdown (Recharts)
- **System Health** — Per-service health status with latency indicators
- **Packet Explorer** — Drill-down view of raw packet → extracted features → ML prediction
- **Analytics** — Historical trend charts and aggregated threat metrics

---

## ⚙️ Tech Stack

### Backend
| Layer | Technology |
|---|---|
| API Framework | FastAPI |
| Data Validation | Pydantic v2 |
| ASGI Server | Uvicorn |
| Language | Python 3.11+ |

### Machine Learning
| Layer | Technology |
|---|---|
| Classifier | Scikit-learn (Random Forest) |
| Numerical Computing | NumPy |
| Model Serialization | Joblib |
| Preprocessing | Scikit-learn Pipeline |

### Frontend
| Layer | Technology |
|---|---|
| Framework | React 18 + Vite |
| Language | TypeScript |
| Styling | TailwindCSS |
| Charts | Recharts |
| HTTP Client | Axios + React Query |

### Infrastructure & Testing
| Layer | Technology |
|---|---|
| Containerization | Docker |
| Testing | Pytest |
| Architecture | Modular Microservices |

---

## 🚀 Local Setup

### Prerequisites

- Python 3.11+
- Node.js 18+ (for dashboard)
- pip / virtualenv

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/aitdp.git
cd aitdp
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate        # Linux / macOS
# venv\Scripts\activate         # Windows
```

### 3. Install Backend Dependencies

```bash
pip install -r requirements.txt
```

### 4. Install Dashboard Dependencies

```bash
cd dashboard
npm install
cd ..
```

---

## ▶️ Running the Platform

Open three separate terminals and start each microservice:

**Terminal 1 — Ingestion Service**
```bash
cd ingestion_service
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

**Terminal 2 — Feature Engine**
```bash
cd feature_engine
uvicorn main:app --host 0.0.0.0 --port 8001 --reload
```

**Terminal 3 — ML Engine**
```bash
cd ml_engine
uvicorn main:app --host 0.0.0.0 --port 8002 --reload
```

**Terminal 4 — Dashboard**
```bash
cd dashboard
npm run dev
```

The dashboard will be available at `http://localhost:5173`.

Alternatively, use the startup script:

```bash
chmod +x scripts/start_services.sh
./scripts/start_services.sh
```

---

## 📡 API Reference

### Ingestion Service `:8000`

#### `GET /health`
```json
{
  "status": "healthy",
  "service": "ingestion_service",
  "timestamp": "2025-01-15T10:30:00Z"
}
```

#### `POST /ingest`

**Request:**
```json
{
  "src_ip": "192.168.1.105",
  "dst_ip": "10.0.0.1",
  "src_port": 54321,
  "dst_port": 22,
  "protocol": "TCP",
  "packet_size": 1420,
  "duration": 0.045,
  "flags": "SYN"
}
```

**Response:**
```json
{
  "status": "accepted",
  "packet_id": "pkt_8f3a2c91",
  "timestamp": "2025-01-15T10:30:01Z"
}
```

---

### Feature Engine `:8001`

#### `POST /extract`

**Request:** *(same packet schema as `/ingest`)*

**Response:**
```json
{
  "features": {
    "protocol_encoded": 0,
    "src_port_category": 2,
    "dst_port_category": 1,
    "is_private_src": 1,
    "is_private_dst": 1,
    "packet_size_normalized": 0.71,
    "duration_normalized": 0.23,
    "risk_score": 0.68,
    "suspicious_flag": 1,
    "connection_direction": 0
  },
  "extraction_time_ms": 2.1
}
```

---

### ML Engine `:8002`

#### `POST /predict`

**Request:** *(feature vector from `/extract`)*

**Response:**
```json
{
  "label": "brute_force",
  "confidence": 0.87,
  "severity": "high",
  "probabilities": {
    "benign": 0.04,
    "dos": 0.05,
    "port_scan": 0.02,
    "brute_force": 0.87,
    "suspicious": 0.02
  },
  "model_version": "rf_v1.2",
  "inference_time_ms": 3.8
}
```

---

## 🧪 Testing

### Run All Tests

```bash
pytest tests/ -v
```

### Run by Category

```bash
# Unit tests
pytest tests/unit/ -v

# API tests
pytest tests/api/ -v

# Integration tests
pytest tests/integration/ -v

# End-to-end pipeline test (packet → prediction)
pytest tests/e2e/test_pipeline.py -v
```

### Smoke Test

```bash
chmod +x scripts/smoke_test.sh
./scripts/smoke_test.sh
```

The smoke test sends a sample packet through the full pipeline and validates the prediction output schema.

### Example E2E Test Flow

```python
# tests/e2e/test_pipeline.py

def test_full_pipeline():
    # Step 1: Ingest packet
    packet = { "src_ip": "192.168.1.10", "dst_ip": "10.0.0.5",
               "src_port": 4444, "dst_port": 22, "protocol": "TCP",
               "packet_size": 800, "duration": 0.02, "flags": "SYN" }
    ingest_response = client.post("http://localhost:8000/ingest", json=packet)
    assert ingest_response.status_code == 200

    # Step 2: Extract features
    extract_response = client.post("http://localhost:8001/extract", json=packet)
    features = extract_response.json()["features"]

    # Step 3: ML prediction
    predict_response = client.post("http://localhost:8002/predict", json=features)
    result = predict_response.json()

    assert result["label"] in ["benign", "dos", "port_scan", "brute_force", "suspicious"]
    assert 0.0 <= result["confidence"] <= 1.0
    assert result["severity"] in ["low", "medium", "high"]
```

---

## 🗺️ Roadmap

AITDP is actively evolving toward a full AI cybersecurity platform. Each phase adds production-grade capabilities that make the system progressively more enterprise-ready.

| Phase | Status | Description |
|---|---|---|
| Phase 1 | ✅ Completed | Packet ingestion microservice |
| Phase 2 | ✅ Completed | Feature engineering engine |
| Phase 3 | ✅ Completed | ML threat detection engine |
| Phase 4 | 🚧 In Progress | Frontend SOC dashboard |
| Phase 5 | 📌 Planned | Database & persistence layer |
| Phase 6 | 📌 Planned | Docker & infrastructure |
| Phase 7 | 📌 Planned | Authentication & security |
| Phase 8 | 📌 Planned | Real-time threat streaming |
| Phase 9 | 📌 Planned | Monitoring & observability |
| Phase 10 | 📌 Planned | Kubernetes deployment |
| Phase 11 | 📌 Planned | Advanced AI enhancements |

### Completed Phases

<details>
<summary><strong>✅ Phase 1 — Packet Ingestion Service</strong></summary>

- FastAPI ingestion microservice
- Packet schema validation with Pydantic
- Request logging with structured output
- Health endpoint
- Modular route architecture

</details>

<details>
<summary><strong>✅ Phase 2 — Feature Engineering Engine</strong></summary>

- ML-ready feature extraction pipeline
- Protocol encoding (TCP / UDP / ICMP / other)
- Source and destination port categorization
- Private / public IP classification
- Connection direction inference
- Suspicious pattern detection
- Risk scoring (0.0 – 1.0 normalized)
- Feature vector normalization
- Modular extractor architecture

</details>

<details>
<summary><strong>✅ Phase 3 — ML Threat Detection Engine</strong></summary>

- Random Forest threat classifier
- Model loading with in-memory caching
- Scikit-learn preprocessing pipeline
- Confidence scoring via class probabilities
- Severity classification (low / medium / high)
- Structured prediction logging
- Training scripts and evaluation scripts
- Saved model artifacts (`.pkl`, `metadata.json`)

</details>

<details>
<summary><strong>🚧 Phase 4 — Frontend Dashboard (In Progress)</strong></summary>

- React + TypeScript + TailwindCSS SOC dashboard
- Live threat monitoring feed
- Severity distribution charts (Recharts)
- System health monitor (per-service status)
- Packet explorer (raw → features → prediction drill-down)
- React Query API integration
- Responsive SOC-style layout

</details>

### Upcoming Phases

<details>
<summary><strong>📌 Phase 5 — Database & Persistence Layer</strong></summary>

- PostgreSQL for packet and prediction storage
- Redis caching for frequently accessed predictions
- Historical packet and threat history APIs
- Analytics persistence for dashboard trends

</details>

<details>
<summary><strong>📌 Phase 6 — Docker & Infrastructure</strong></summary>

- Docker Compose full-stack orchestration
- Container networking between services
- Environment variable management
- Production-ready build configuration

</details>

<details>
<summary><strong>📌 Phase 7 — Authentication & Security</strong></summary>

- JWT-based API authentication
- Role-based access control (RBAC)
- Protected dashboard routes
- API key management

</details>

<details>
<summary><strong>📌 Phase 8 — Real-Time Threat Streaming</strong></summary>

- WebSocket integration across services
- Live threat feed in dashboard (sub-second updates)
- Real-time alert push notifications
- Streaming packet monitoring

</details>

<details>
<summary><strong>📌 Phase 9 — Monitoring & Observability</strong></summary>

- Prometheus metrics endpoints on all services
- Grafana dashboard integration
- Centralized structured logging pipeline
- Service latency and throughput monitoring

</details>

<details>
<summary><strong>📌 Phase 10 — Kubernetes Deployment</strong></summary>

- Kubernetes manifests for all microservices
- Helm chart packaging
- Horizontal pod autoscaling
- Cloud-native deployment (GKE / EKS / AKS ready)

</details>

<details>
<summary><strong>📌 Phase 11 — Advanced AI Enhancements</strong></summary>

- Anomaly detection models (Isolation Forest / Autoencoder)
- Deep learning integration (LSTM for sequence-based threat detection)
- Behavioral analytics and session-level profiling
- Ensemble threat detection (RF + gradient boosting)
- Adaptive risk scoring with feedback loops

</details>

---

## 📈 Scalability Design

AITDP is architected for horizontal scalability at every layer:

- **Service Independence** — Each microservice scales independently based on load; the ML engine can be replicated without touching the ingestion or feature layers.
- **Stateless Services** — All three services are stateless by design, making them load-balancer-friendly.
- **Model Caching** — The ML engine caches the loaded model in memory, eliminating per-request disk I/O.
- **Queue-Ready** — The ingestion → feature → ML pipeline can be decoupled with a message queue (Kafka / RabbitMQ) in a future phase with no service-level changes.
- **Container-First** — Every service is containerized, supporting Kubernetes HPA-based scaling in Phase 10.
- **Database-Ready** — The persistence layer is isolated to Phase 5, meaning the existing services require no architectural changes to support it.

---

## 🔐 Security Design Philosophy

AITDP applies security-first thinking at the design level:

- **Schema Enforcement** — All incoming payloads are validated via Pydantic schemas before processing begins; malformed or missing fields are rejected at the ingestion boundary.
- **No Trust Between Services** — Services communicate over defined API contracts and do not share internal state or memory.
- **Structured Logging** — All requests, predictions, and errors are logged in structured JSON format for auditability.
- **Severity Routing** — High-severity threats are classified and flagged in the prediction response, enabling downstream alert escalation.
- **Auth Layer (Phase 7)** — JWT authentication and RBAC are planned as a dedicated phase to avoid bolting on security as an afterthought.

---

## 🤝 Contributing

Contributions are welcome. If you'd like to extend AITDP — add a new threat classifier, build a dashboard panel, or implement a planned phase — please follow this process:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/phase-5-postgres`
3. Commit your changes with clear messages
4. Open a pull request with a description of what was added and why

For significant architectural changes, please open an issue first to align on the approach before implementation.

---

## 📄 License

This project is licensed under the **MIT License**. See [`LICENSE`](./LICENSE) for full terms.

---

<div align="center">

**AITDP** — Built to mirror the architecture of modern AI-powered cybersecurity platforms.

*Actively engineered. Incrementally scaled. Production-oriented.*

</div>
