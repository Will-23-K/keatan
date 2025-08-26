import json, math
from datetime import datetime
from random import random

# Load site catalog from sites.json if present; otherwise use built-in minimal list
try:
    with open("sites.json","r") as f:
        SITES = json.load(f)
except:
    SITES = [
        {"id":"site-za-hydro","name":"South Africa - Hydro Grid","region":"ZA","capacity_mw":50,"cost_per_kwh":0.04,"carbon_gco2_per_kwh":50,"renewable_pct":0.9},
        {"id":"site-iceland","name":"Iceland - Geothermal","region":"IS","capacity_mw":40,"cost_per_kwh":0.03,"carbon_gco2_per_kwh":10,"renewable_pct":0.98},
        {"id":"site-norway","name":"Norway - Hydro+Wind","region":"NO","capacity_mw":60,"cost_per_kwh":0.035,"carbon_gco2_per_kwh":20,"renewable_pct":0.95},
        {"id":"site-us-solar","name":"US Southwest - Solar + Storage","region":"US","capacity_mw":30,"cost_per_kwh":0.025,"carbon_gco2_per_kwh":40,"renewable_pct":0.8}
    ]

def score_site_for_job(site, job):
    """
    Score a site lower-is-better based on cost, carbon, and ability to satisfy urgency.
    """
    # Estimate energy consumption: assume cores consume ~0.3 kW per core under load (simplified)
    est_power_kw = job["cores"] * 0.3
    est_energy_kwh = est_power_kw * job["hours"]  # kWh

    cost = est_energy_kwh * site["cost_per_kwh"]
    carbon = est_energy_kwh * site["carbon_gco2_per_kwh"]

    # Urgency penalty: sites with lower renewable_pct can be penalized if urgent (to prefer readily dispatchable energy)
    urgency = job.get("urgency",5)  # 1-10 (10 is most urgent)
    renewable_factor = site.get("renewable_pct",0.5)
    dispatch_score = max(0.01, 1.0 - renewable_factor) * (urgency/10.0)

    # capacity headroom heuristic: penalize if requested cores would correspond to >5% of site capacity (very rough)
    requested_mw = (est_power_kw/1000.0)
    capacity_frac = requested_mw / max(0.001, site["capacity_mw"])
    capacity_penalty = max(0, capacity_frac - 0.05) * 100.0

    # model size multiplier (large models are more sensitive to latency/cost)
    ms = job.get("model_size","medium")
    ms_mul = {"small":0.9,"medium":1.0,"large":1.2}.get(ms,1.0)

    # final score combines normalized cost, carbon, dispatch, capacity penalty
    score = (cost * 1.0) + (carbon * 0.02) + (dispatch_score * 10.0) + capacity_penalty
    score *= ms_mul

    # Add small randomness to break ties
    score *= (0.98 + 0.04 * random())

    return {
        "site_id": site["id"],
        "site_name": site["name"],
        "region": site.get("region",""),
        "estimated_cost_usd": round(cost,4),
        "estimated_carbon_gco2": round(carbon,2),
        "score": round(score,4)
    }

def recommend_site(job, top_k=3):
    scored = [score_site_for_job(s, job) for s in SITES]
    scored_sorted = sorted(scored, key=lambda x: x["score"])
    return {"job": job, "recommendations": scored_sorted[:top_k], "timestamp": datetime.utcnow().isoformat()+"Z"}