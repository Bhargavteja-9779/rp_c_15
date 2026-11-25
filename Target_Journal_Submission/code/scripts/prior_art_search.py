#!/usr/bin/env python
"""Run the logged prior-art queries (>= 8 phrasings per claim) against arXiv and Crossref; append to state/novelty_ledger.json."""
import json
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

R = Path(__file__).resolve().parents[1]
LED = R / "state" / "novelty_ledger.json"
CLAIMS = {
 "C1": ["prediction interval coverage near infrared fruit new season", "conformal prediction NIR spectroscopy distribution shift", "uncertainty quantification NIR calibration season robustness fruit",
        "conformal prediction chemometrics calibration transfer", "prediction intervals dry matter mango NIR", "coverage of prediction intervals spectroscopy external validation",
        "uncertainty dry matter fruit spectroscopy deep ensemble", "conformal prediction agriculture spectroscopy"],
 "C2": ["few-shot conformal prediction labeled target samples regression", "conformal prediction hierarchical grouped data group exchangeability", "conformal prediction few labeled samples new domain bias correction",
        "conformal recalibration small target calibration set", "conformal prediction random effects groups prediction set", "meta-learning conformal prediction tasks calibration",
        "conformal prediction repeated measurements scale normalized score", "test-time adaptation conformal prediction few labels"],
 "C3": ["PAC prediction sets meta learning tasks", "conformal prediction training-conditional coverage per group guarantee", "group-conditional coverage conformal prediction",
        "conformal prediction coverage for most groups high probability", "tolerance intervals grouped data distribution-free", "second-moment coverage conformal hierarchical",
        "mondrian conformal prediction groups", "conformal prediction cluster coverage guarantee"],
 "C4": ["sample size calibration conformal prediction width planning", "how many labeled samples to recalibrate model new domain", "optimal number of reference samples NIR calibration maintenance",
        "spiking NIR calibration local samples number", "slope bias correction number of samples NIR", "active labeling conformal prediction budget",
        "label budget calibration under distribution shift", "conformal prediction interval width as function of calibration size"],
 "C5": ["conformal prediction decision making cost sensitive threshold", "harvest decision dry matter threshold NIR uncertainty", "risk control conformal decision agriculture",
        "conformal risk control decision", "fruit maturity harvest decision support spectroscopy", "lower confidence bound acceptance decision quality grading",
        "decision-theoretic conformal prediction", "NIR grading fruit misclassification cost"],
}


def arxiv(q, n=8):
    u = "https://export.arxiv.org/api/query?" + urllib.parse.urlencode({"search_query": f"all:{q}", "max_results": n})
    x = urllib.request.urlopen(u, timeout=60).read()
    ns = {"a": "http://www.w3.org/2005/Atom"}
    out = []
    for e in ET.fromstring(x).findall("a:entry", ns):
        out.append({"source": "arXiv", "id": e.find("a:id", ns).text.split("/abs/")[-1], "title": " ".join(e.find("a:title", ns).text.split()),
                    "year": e.find("a:published", ns).text[:4], "abstract": " ".join(e.find("a:summary", ns).text.split())[:600]})
    return out


def crossref(q, n=8):
    u = "https://api.crossref.org/works?" + urllib.parse.urlencode({"query.bibliographic": q, "rows": n, "select": "DOI,title,issued,container-title,abstract"})
    d = json.load(urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "research-script/1.0"}), timeout=60))
    return [{"source": "Crossref", "id": it["DOI"], "title": (it.get("title") or [""])[0], "year": str(it.get("issued", {}).get("date-parts", [[None]])[0][0]),
             "venue": (it.get("container-title") or [""])[0]} for it in d["message"]["items"]]


led = json.loads(LED.read_text()) if LED.exists() else {"queries": [], "papers_opened": {}, "claims": {}}
done = {(q["claim"], q["query"], q["engine"]) for q in led["queries"]}
for c, qs in CLAIMS.items():
    for q in qs:
        for eng, fn in (("arXiv", arxiv), ("Crossref", crossref)):
            if (c, q, eng) in done:
                continue
            try:
                hits = fn(q)
            except Exception as e:
                hits = [{"error": repr(e)}]
            led["queries"].append({"claim": c, "query": q, "engine": eng, "date": time.strftime("%Y-%m-%d"), "hits": hits})
            time.sleep(3 if eng == "arXiv" else 1)
LED.write_text(json.dumps(led, indent=1))
print(sum(1 for q in led["queries"]), "queries logged")
