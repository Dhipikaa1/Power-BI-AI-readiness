#!/usr/bin/env python3
"""AI-Readiness Score for a Power BI semantic model (TMDL).

Parses the model's ``tables/*.tmdl`` files and scores how ready the model is for
Copilot / natural-language consumption, against eight weighted rules (total 100).
Standard library only.

Usage:
    python ai_readiness_score.py <path-to .SemanticModel or definition folder> [--out result.json]
"""

import argparse
import json
import re
import sys
from pathlib import Path

# Rule weights (sum = 100).
WEIGHTS = {
    "measure_descriptions": 14,
    "column_descriptions": 12,
    "table_descriptions": 8,
    "business_friendly_names": 14,
    "keys_hidden": 8,
    "keys_summarize_none": 5,
    "measure_format_strings": 7,
    "synonyms": 8,
    "date_table_marked": 8,
    "single_direction_relationships": 8,
    "correct_types": 8,
}


def _unquote(name):
    name = name.strip()
    if name.startswith("'") and name.endswith("'"):
        name = name[1:-1]
    return name


def _is_key(source, name):
    token = (source or name or "").lower()
    return token.endswith("id") or token.endswith("ky") or "key" in token


def _is_time_grain(source, name):
    token = (source or name or "").lower()
    return token in {"yr", "mth", "qtr", "year", "month", "quarter"}


def _is_int_like(source, name):
    return _is_key(source, name) or _is_time_grain(source, name) or \
        (source or name or "").lower() in {"qty", "quantity"}


def _friendly(name):
    return "_" not in name and (" " in name or name[:1].isupper())


def parse_tables(definition_dir):
    tables = []
    tdir = definition_dir / "tables"
    for path in sorted(tdir.glob("*.tmdl")):
        table = None
        obj = None
        pending_doc = False
        in_partition = False
        for raw in path.read_text(encoding="utf-8").splitlines():
            indent = len(raw) - len(raw.lstrip("\t"))
            s = raw.strip()
            if not s:
                continue
            if s.startswith("///"):
                pending_doc = True
                continue
            if indent == 0 and s.startswith("table "):
                table = {"name": _unquote(s[6:]), "desc": pending_doc, "dataCategory": None,
                         "columns": [], "measures": []}
                tables.append(table)
                obj, in_partition, pending_doc = None, False, False
                continue
            if table is None:
                pending_doc = False
                continue
            if indent == 1 and s.startswith("column "):
                obj = {"name": _unquote(s[7:]), "desc": pending_doc, "hidden": False,
                       "summarizeBy": None, "formatString": None, "source": None,
                       "dataType": None, "synonyms": False}
                table["columns"].append(obj)
                in_partition, pending_doc = False, False
                continue
            if indent == 1 and s.startswith("measure "):
                name = s[8:].split("=", 1)[0]
                obj = {"name": _unquote(name), "desc": pending_doc,
                       "formatString": None, "synonyms": False}
                table["measures"].append(obj)
                in_partition, pending_doc = False, False
                continue
            if indent == 1 and s.startswith("partition "):
                obj, in_partition, pending_doc = None, True, False
                continue
            if indent == 1 and s.startswith("dataCategory:"):
                table["dataCategory"] = s.split(":", 1)[1].strip()
                obj, pending_doc = None, False
                continue
            if indent == 1:
                obj, pending_doc = None, False
                continue
            if in_partition or obj is None:
                continue
            if s == "isHidden" or s.startswith("isHidden"):
                obj["hidden"] = True
            elif s.startswith("summarizeBy:"):
                obj["summarizeBy"] = s.split(":", 1)[1].strip()
            elif s.startswith("formatString:"):
                obj["formatString"] = s.split(":", 1)[1].strip()
            elif s.startswith("dataType:"):
                obj["dataType"] = s.split(":", 1)[1].strip()
            elif s.startswith("sourceColumn:"):
                obj["source"] = s.split(":", 1)[1].strip()
            elif s.startswith("annotation Synonyms"):
                obj["synonyms"] = True
        continue
    return tables


def parse_relationships(definition_dir):
    rels = []
    path = definition_dir / "relationships.tmdl"
    if not path.exists():
        return rels
    cur = None
    for raw in path.read_text(encoding="utf-8").splitlines():
        s = raw.strip()
        if s.startswith("relationship "):
            cur = {"name": s[len("relationship "):].strip(), "cross": "single"}
            rels.append(cur)
        elif cur is not None and s.startswith("crossFilteringBehavior:"):
            cur["cross"] = s.split(":", 1)[1].strip()
    return rels


def _pct(hits, total):
    return 1.0 if total == 0 else hits / total


def score(definition_dir):
    tables = parse_tables(definition_dir)
    rels = parse_relationships(definition_dir)
    measures = [m for t in tables for m in t["measures"]]
    vis_cols = [c for t in tables for c in t["columns"] if not c["hidden"]]
    all_cols = [c for t in tables for c in t["columns"]]
    keys = [c for c in all_cols if _is_key(c["source"], c["name"])]
    grain = [c for c in all_cols if _is_key(c["source"], c["name"]) or _is_time_grain(c["source"], c["name"])]
    int_like = [c for c in all_cols if _is_int_like(c["source"], c["name"])]
    date_marked = any((t.get("dataCategory") or "").lower() == "time" for t in tables)

    fr = {
        "measure_descriptions": _pct(sum(m["desc"] for m in measures), len(measures)),
        "column_descriptions": _pct(sum(c["desc"] for c in vis_cols), len(vis_cols)),
        "table_descriptions": _pct(sum(t["desc"] for t in tables), len(tables)),
        "business_friendly_names": _pct(
            sum(_friendly(t["name"]) for t in tables)
            + sum(_friendly(c["name"]) for c in vis_cols)
            + sum(_friendly(m["name"]) for m in measures),
            len(tables) + len(vis_cols) + len(measures)),
        "keys_hidden": _pct(sum(c["hidden"] for c in keys), len(keys)),
        "keys_summarize_none": _pct(
            sum((c["summarizeBy"] or "").lower() == "none" for c in grain), len(grain)),
        "measure_format_strings": _pct(sum(bool(m["formatString"]) for m in measures), len(measures)),
        "synonyms": _pct(
            sum(t.get("synonyms", False) for t in tables)
            + sum(c["synonyms"] for c in vis_cols)
            + sum(m["synonyms"] for m in measures),
            len(tables) + len(vis_cols) + len(measures)),
        "date_table_marked": 1.0 if date_marked else 0.0,
        "single_direction_relationships": _pct(
            sum((r["cross"] or "single").lower() != "bothdirections" for r in rels), len(rels)),
        "correct_types": _pct(
            sum((c["dataType"] or "int64").lower() == "int64" for c in int_like), len(int_like)),
    }
    breakdown = {k: {"coverage": round(fr[k], 3), "weight": WEIGHTS[k],
                     "points": round(fr[k] * WEIGHTS[k], 1)} for k in WEIGHTS}
    total = round(sum(b["points"] for b in breakdown.values()), 1)
    return {
        "model": definition_dir.parent.name,
        "counts": {"tables": len(tables), "visible_columns": len(vis_cols),
                   "measures": len(measures), "key_columns": len(keys),
                   "relationships": len(rels)},
        "breakdown": breakdown,
        "score": total,
    }


def _resolve_definition(path):
    path = Path(path)
    if (path / "definition" / "tables").is_dir():
        return path / "definition"
    if (path / "tables").is_dir():
        return path
    raise SystemExit(f"Could not find a definition/tables folder under: {path}")


def main():
    ap = argparse.ArgumentParser(description="AI-Readiness Score for a Power BI model (TMDL).")
    ap.add_argument("model", help="Path to the .SemanticModel folder or its definition folder")
    ap.add_argument("--out", help="Write the result JSON to this path")
    args = ap.parse_args()

    result = score(_resolve_definition(args.model))
    print(f"\nAI-Readiness Score for '{result['model']}': {result['score']} / 100")
    print(f"  {result['counts']}")
    for rule, b in result["breakdown"].items():
        bar = "#" * int(b["coverage"] * 20)
        print(f"  {rule:26s} {b['points']:5.1f}/{b['weight']:<3}  [{bar:<20}] {int(b['coverage']*100)}%")
    if args.out:
        Path(args.out).parent.mkdir(parents=True, exist_ok=True)
        Path(args.out).write_text(json.dumps(result, indent=2), encoding="utf-8")
        print(f"\nSaved: {args.out}")
    return result


if __name__ == "__main__":
    main()
