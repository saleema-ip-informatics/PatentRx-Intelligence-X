"""EGFR patent assay analysis; no binding or clinical efficacy inference."""
import math

ENDPOINTS = {
    "egfr_wt", "egfr_exon19del", "egfr_l858r", "pc9", "a431"
}

def analyze_measurement(measurement: dict) -> dict:
    status = measurement["status"]
    value = measurement["value_nM"]

    if status in {"blank", "not_tested"}:
        if value is not None:
            raise ValueError("Missing measurement must have null value")
        return {"status": status, "pic50": None}

    if status not in {"exact", "less_than"}:
        raise ValueError("Unknown measurement status")

    if not isinstance(value, (int, float)) or isinstance(value, bool):
        raise ValueError("IC50 must be numeric")
    if not math.isfinite(value) or value <= 0:
        raise ValueError("IC50 must be finite and positive")

    pic50 = 9 - math.log10(value)

    if status == "less_than":
        return {
            "status": status,
            "ic50_upper_bound_nM": value,
            "pic50_lower_bound": pic50,
            "pic50": None,
        }

    return {"status": status, "pic50": pic50}


def compare_potency(a: dict, b: dict, endpoint_a: str, endpoint_b: str) -> dict:
    if endpoint_a not in ENDPOINTS or endpoint_b not in ENDPOINTS:
        raise ValueError("Unknown assay endpoint")
    if endpoint_a != endpoint_b:
        return {"comparable": False, "reason": "Different assay endpoints"}

    x, y = analyze_measurement(a), analyze_measurement(b)
    if x["status"] != "exact" or y["status"] != "exact":
        return {"comparable": False, "reason": "Non-exact measurement"}

    return {
        "comparable": True,
        "potency_ratio_a_over_b": b["value_nM"] / a["value_nM"],
        "delta_pic50_a_minus_b": x["pic50"] - y["pic50"],
    }
