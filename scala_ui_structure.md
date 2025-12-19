Scala UI Structure (conceptual)
================================

Goal: a lightweight Scala service (Play Framework or Akka HTTP) that reads the predictions Parquet/CSV and renders interactive charts (e.g., using Plotly.js or Chart.js on the frontend).

Suggested project layout

- `ui/`
  - `build.sbt` (Play or sbt config)
  - `app/`
    - `controllers/PredictionController.scala`  -- provides REST endpoints like `/predictions` and `/metrics`
    - `services/PredictionService.scala`        -- reads CSV/Parquet and caches recent results
    - `views/`                                 -- Twirl templates or static HTML serving SPA
  - `public/`                                  -- JS/CSS assets (Chart.js, Plotly)

Key endpoints (HTTP)
- `GET /metrics` -> returns JSON {rmse, mae}
- `GET /predictions?limit=100` -> returns recent predicted vs actual rows

Implementation notes
- Use Apache Parquet reader (e.g., Apache Arrow or spark-submit sidecar) or convert predictions to an API-friendly CSV/JSON for the UI to consume.
- For interactivity, serve a small SPA (React/Vue) that calls `/predictions` and draws charts with Chart.js or Plotly.

Security & Deployment
- Containerize backend with Docker; mount prediction files as a volume.
- Serve behind a reverse proxy (NGINX) if exposing publicly.
