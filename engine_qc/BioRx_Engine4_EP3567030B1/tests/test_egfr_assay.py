import json
import math
from pathlib import Path

import pytest

from patentrx.engines.biorx.egfr_assay import (
    analyze_measurement,
    compare_potency,
)

DATA = (
    Path(__file__).resolve().parents[1]
    / "data/patent_assay_normalized.json"
)


@pytest.mark.parametrize("ic50,expected", [
    (1, 9),
    (10, 8),
    (100, 7),
])
def test_pic50_conversion(ic50, expected):
    result = analyze_measurement({"status": "exact", "value_nM": ic50})
    assert math.isclose(result["pic50"], expected)


def test_censored_measurement():
    result = analyze_measurement({
        "status": "less_than",
        "value_nM": 0.015,
    })
    assert result["pic50"] is None
    assert math.isclose(
        result["pic50_lower_bound"],
        9 - math.log10(0.015),
    )


def test_same_endpoint_potency():
    a = {"status": "exact", "value_nM": 10}
    b = {"status": "exact", "value_nM": 100}
    result = compare_potency(a, b, "pc9", "pc9")
    assert result["comparable"]
    assert math.isclose(result["potency_ratio_a_over_b"], 10)
    assert math.isclose(result["delta_pic50_a_minus_b"], 1)


def test_cross_endpoint_not_comparable():
    a = {"status": "exact", "value_nM": 10}
    b = {"status": "exact", "value_nM": 100}
    assert not compare_potency(a, b, "pc9", "a431")["comparable"]


@pytest.mark.parametrize("value", [0, -1, float("nan"), float("inf")])
def test_invalid_ic50(value):
    with pytest.raises(ValueError):
        analyze_measurement({"status": "exact", "value_nM": value})


def test_patent_dataset():
    data = json.loads(DATA.read_text(encoding="utf-8"))
    assert len(data["records"]) == 34

    counts = {}
    for record in data["records"]:
        assert len(record["measurements"]) == 5
        for measurement in record["measurements"].values():
            result = analyze_measurement(measurement)
            status = result["status"]
            counts[status] = counts.get(status, 0) + 1

    assert counts == {
        "exact": 60,
        "less_than": 2,
        "not_tested": 107,
        "blank": 1,
    }
