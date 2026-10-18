import json
from pathlib import Path
from collections import Counter

root = Path(__file__).resolve().parents[1]
source = root / "data/patent_assay_raw.json"
output = root / "data/patent_assay_normalized.json"

if output.exists():
    raise SystemExit(f"STOP: preserving existing file: {output}")

data = json.loads(source.read_text(encoding="utf-8"))
endpoints = ["egfr_wt", "egfr_exon19del", "egfr_l858r", "pc9", "a431"]
records = []
counts = Counter()

for table in data["tables"]:
    for row in table["rows"][1:]:
        if not row[0] or row[0].startswith("Note:"):
            continue

        measurements = {}
        for endpoint, raw in zip(endpoints, row[1:]):
            value_text = (raw or "").strip()

            if not value_text:
                status, value = "blank", None
            elif value_text == "-":
                status, value = "not_tested", None
            elif value_text.startswith("<"):
                status, value = "less_than", float(value_text[1:])
            else:
                status, value = "exact", float(value_text)

            measurements[endpoint] = {
                "status": status,
                "value_nM": value,
                "raw": value_text,
            }
            counts[status] += 1

        records.append({
            "compound": " ".join(row[0].split()),
            "pdf_page": table["pdf_page"],
            "measurements": measurements,
        })

assert len(records) == 34
assert all(len(r["measurements"]) == 5 for r in records)
assert counts["blank"] == 1
assert counts["less_than"] == 2

output.write_text(
    json.dumps({"patent": "EP3567030B1", "records": records}, indent=2),
    encoding="utf-8",
)
print("CREATED:", output)
print("COMPOUNDS:", len(records))
print("ASSAY CELLS:", sum(counts.values()))
print("MEASUREMENT STATUS:", dict(counts))
