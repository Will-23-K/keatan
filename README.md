GaiaGrid Prototype - Carbon-aware Compute Scheduler
==================================================

What this is
------------
A minimal prototype demonstrating the core app idea: a scheduler that recommends compute sites
based on simulated cost, carbon intensity, renewable availability and job parameters.

Files
-----
- app.py              : Flask web app (entrypoint)
- scheduler.py        : Carbon-aware scheduling logic
- sites.json          : Example site catalog (regions, costs, carbon)
- templates/index.html: Simple web UI
- requirements.txt    : Python dependencies
- README.md           : this file

Run locally (dev)
-----------------
1. Create a Python 3.10+ virtualenv
   python -m venv venv
   source venv/bin/activate   # or venv\\Scripts\\activate on Windows

2. Install dependencies
   pip install -r requirements.txt

3. Run the app
   python app.py

4. Open http://localhost:8501 in your browser

Notes & Next steps
------------------
- This is a prototype for demonstration. Productionizing requires secure APIs, multi-tenant auth,
  billing, real-time telemetry integration with energy providers, verifiable attestation, and hardware ops.
- I can help generate Dockerfiles, K8s manifests, Terraform configs, and a deployment plan next.