Architecture Diagram

Binance Futures Exchange
        │
        │  (Live Trade Data via WebSocket)
        ▼
Data Ingestion Layer
(backend/ingest.py)
        │
        │  Cleaned Tick Data
        ▼
Storage Layer
(SQLite Database - ticks.db)
        │
        │  Time-Series Queries
        ▼
Analytics Layer
(backend/analytics.py)
        │
        │  Computed Metrics
        ▼
Presentation Layer
(Streamlit Dashboard - frontend/app.py)
