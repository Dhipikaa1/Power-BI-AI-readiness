"""
Runs the sempy notebook's exact 7-category scoring logic against the local before/after
TMDL (offline), so we can report the numbers without a live Fabric workspace.

The scoring helper functions and category formulas are copied verbatim from
scoring/AI_Readiness_Score.ipynb; only the data source is swapped (TMDL parse instead
of sempy.fabric.list_*).
"""
import os, re, glob

ROOT = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------- TMDL parser
def parse_model(defn_dir):
    tables, columns, measures = [], [], []
    for path in glob.glob(os.path.join(defn_dir, "tables", "*.tmdl")):
        lines = open(path, encoding="utf-8").read().splitlines()
        pending_desc = []
        tname, tdesc, tcat = None, "", ""
        i = 0
        while i < len(lines):
            raw = lines[i]
            stripped = raw.strip()
            depth = len(raw) - len(raw.lstrip("\t"))
            if stripped.startswith("/// "):
                pending_desc.append(stripped[4:])
                i += 1; continue
            if depth == 0 and stripped.startswith("table "):
                tname = stripped[len("table "):].strip().strip("'")
                tdesc = " ".join(pending_desc); pending_desc = []
                i += 1; continue
            if depth == 1 and stripped.startswith("dataCategory:"):
                tcat = stripped.split(":", 1)[1].strip()
                i += 1; continue
            if depth == 1 and stripped.startswith("column "):
                rest = stripped[len("column "):].strip()
                is_calc = "=" in rest
                cname = (rest.split("=", 1)[0] if is_calc else rest).strip().strip("'")
                desc = " ".join(pending_desc); pending_desc = []
                attrs = {"Data Type": None, "Is Hidden": False, "Format String": "",
                         "Summarize By": "", "Column Type": "Calculated" if is_calc else "Data"}
                j = i + 1
                while j < len(lines):
                    a = lines[j]
                    ad = len(a) - len(a.lstrip("\t"))
                    if a.strip() == "":
                        j += 1; continue
                    if ad < 2:
                        break
                    s = a.strip()
                    if s.startswith("dataType:"):
                        attrs["Data Type"] = s.split(":", 1)[1].strip()
                    elif s == "isHidden":
                        attrs["Is Hidden"] = True
                    elif s.startswith("formatString:"):
                        attrs["Format String"] = s.split(":", 1)[1].strip()
                    elif s.startswith("summarizeBy:"):
                        attrs["Summarize By"] = s.split(":", 1)[1].strip()
                    j += 1
                columns.append({"Table Name": tname, "Column Name": cname,
                                "Description": desc, **attrs})
                i = j; continue
            if depth == 1 and stripped.startswith("measure "):
                rest = stripped[len("measure "):]
                mname, expr = rest.split("=", 1)
                mname = mname.strip().strip("'")
                expr = expr.strip()
                desc = " ".join(pending_desc); pending_desc = []
                fmt = ""
                j = i + 1
                while j < len(lines):
                    a = lines[j]
                    ad = len(a) - len(a.lstrip("\t"))
                    if a.strip() == "":
                        j += 1; continue
                    if ad < 2:
                        break
                    s = a.strip()
                    if s.startswith("formatString:"):
                        fmt = s.split(":", 1)[1].strip()
                    j += 1
                measures.append({"Table Name": tname, "Measure Name": mname,
                                 "Measure Expression": expr, "Description": desc,
                                 "Format String": fmt})
                i = j; continue
            if stripped == "" or stripped.startswith("annotation") or stripped.startswith("partition") \
               or stripped.startswith("ref ") or stripped.startswith("source") or stripped.startswith("mode:"):
                pending_desc = [] if stripped.startswith("partition") else pending_desc
            i += 1
        if tname:
            tables.append({"Name": tname, "Description": tdesc, "dataCategory": tcat})

    # relationships
    rels = []
    rp = os.path.join(defn_dir, "relationships.tmdl")
    if os.path.exists(rp):
        blocks = re.split(r"\n(?=relationship )", open(rp, encoding="utf-8").read())
        for b in blocks:
            if not b.strip().startswith("relationship"):
                continue
            cf = "BothDirections" if re.search(r"crossFilteringBehavior:\s*bothDirections", b) else "OneDirection"
            fc = re.search(r"fromColumn:\s*(.+)", b)
            tc = re.search(r"toColumn:\s*(.+)", b)
            frm = fc.group(1).strip() if fc else ""
            to = tc.group(1).strip() if tc else ""
            from_card = "Many" if re.search(r"fromCardinality:\s*many", b) else ("One" if re.search(r"fromCardinality:\s*one", b) else "Many")
            to_card = "One" if not re.search(r"toCardinality:\s*many", b) else "Many"
            rels.append({"From Table": frm.split(".")[0], "From Column": frm,
                         "To Table": to.split(".")[0], "To Column": to,
                         "Cross Filtering Behavior": cf, "From Cardinality": from_card,
                         "To Cardinality": to_card, "Is Active": True})
    return tables, columns, measures, rels


# ---------------------------------------------------- helpers (verbatim from notebook)
def is_business_friendly(name):
    if not name or len(name) <= 2:
        return False
    if re.match(r'^(vw|tbl|dim_|fact_|stg_|src_|dbo_|raw_)', name, re.IGNORECASE):
        return False
    if name == name.upper() and len(name) > 3:
        return False
    if name.count('_') > 2:
        return False
    if re.search(r'[0-9a-f]{8}-[0-9a-f]{4}', name, re.IGNORECASE):
        return False
    return True


def classify_table(name):
    n = name.lower()
    if n.startswith('localdatetable_') or n.startswith('datetabletemplate_'):
        return 'Auto-generated'
    if 'bridge' in n:
        return 'Bridge'
    if n.startswith('parameter'):
        return 'Field Parameter'
    if 'measures' in n and 'table' in n:
        return 'Measures Only'
    if n == 'datarefresh' or 'refresh' in n or 'freshness' in n:
        return 'Utility'
    if 'date' in n or 'calendar' in n:
        return 'Date Dimension'
    if 'fact' in n:
        return 'Fact'
    if 'dim' in n:
        return 'Dimension'
    return 'Other'


def has_description(desc):
    if desc is None:
        return False
    return str(desc).strip() != ''


def detect_antipatterns(expression):
    if not expression or expression.strip() == '':
        return []
    dax = expression
    issues = []
    if re.findall(r'(?<![/"\'])\/(?![/\*])', dax):
        issues.append("uses / instead of DIVIDE()")
    if re.search(r'\bFILTER\s*\(\s*(?!ALL\b|VALUES\b|DISTINCT\b|ADDCOLUMNS\b|SELECTCOLUMNS\b|SUMMARIZE\b|UNION\b|DATATABLE\b|FILTER\b|GENERATESERIES\b)[A-Z][A-Za-z_\s]+,', dax, re.IGNORECASE):
        issues.append("FILTER on full table")
    if len(re.findall(r'\bIF\s*\(', dax, re.IGNORECASE)) > 3:
        issues.append("nested IF")
    if re.search(r'\bEARLIER\b|\bEARLIEST\b', dax, re.IGNORECASE):
        issues.append("EARLIER/EARLIEST")
    if re.search(r'\bCALCULATE\s*\([^)]*\bCALCULATE\s*\(', dax, re.IGNORECASE):
        issues.append("nested CALCULATE")
    if re.search(r'\bCOUNTROWS\s*\(\s*FILTER\s*\(', dax, re.IGNORECASE):
        issues.append("COUNTROWS(FILTER(...))")
    if re.search(r'\bCALCULATE\s*\(.*\bFILTER\s*\(\s*ALL\s*\(', dax, re.IGNORECASE | re.DOTALL):
        issues.append("FILTER(ALL(...))")
    if re.search(r'\b(SUMX|AVERAGEX|MAXX|MINX|RANKX|PRODUCTX|CONCATENATEX)\s*\(\s*(?!ALL\b|VALUES\b|DISTINCT\b|FILTER\b|ADDCOLUMNS\b|SELECTCOLUMNS\b|SUMMARIZE\b|TOPN\b|GENERATESERIES\b)[A-Z][A-Za-z_\s]+,', dax, re.IGNORECASE):
        issues.append("iterator on unfiltered table")
    if len(dax) > 200 and not re.search(r'\bVAR\b', dax, re.IGNORECASE):
        issues.append("complex DAX without VAR/RETURN")
    return issues


def detect_complexity(expression):
    if not expression or expression.strip() == '':
        return []
    dax = expression
    issues = []
    max_depth = depth = 0
    for ch in dax:
        if ch == '(':
            depth += 1; max_depth = max(max_depth, depth)
        elif ch == ')':
            depth -= 1
    if max_depth > 8:
        issues.append("deep nesting")
    elif max_depth > 5:
        issues.append("moderate nesting")
    if len(re.findall(r'\bCALCULATE\b', dax, re.IGNORECASE)) > 3:
        issues.append("too many CALCULATE")
    if len(re.findall(r'\bFILTER\b', dax, re.IGNORECASE)) > 3:
        issues.append("too many FILTER")
    if len(dax) > 1000:
        issues.append("very long")
    elif len(dax) > 500:
        issues.append("long")
    return issues


# ---------------------------------------------------- 7-category scorer (notebook logic)
def score(defn_dir):
    tables, columns, measures, rels = parse_model(defn_dir)
    tables_total, cols_total, meas_total = len(tables), len(columns), len(measures)

    # 1 Description Coverage
    tdesc = sum(has_description(t["Description"]) for t in tables)
    cdesc = sum(has_description(c["Description"]) for c in columns)
    mdesc = sum(has_description(m["Description"]) for m in measures)
    total_obj = tables_total + cols_total + meas_total
    desc_score = (tdesc + cdesc + mdesc) / max(total_obj, 1) * 100

    # 2 Naming Quality
    all_names = ([t["Name"] for t in tables] + [c["Column Name"] for c in columns] +
                 [m["Measure Name"] for m in measures])
    good = sum(is_business_friendly(str(n)) for n in all_names)
    naming_score = good / max(len(all_names), 1) * 100

    # 3 Relationship Health
    bidi = mm = mmb = 0
    for r in rels:
        is_bidi = 'both' in r["Cross Filtering Behavior"].lower()
        is_mm = 'many' in r["From Cardinality"].lower() and 'many' in r["To Cardinality"].lower()
        if is_mm and is_bidi: mmb += 1
        elif is_mm: mm += 1
        elif is_bidi: bidi += 1
    penalty = mmb * 30 + mm * 20 + bidi * 15
    rel_health = 100.0 if penalty == 0 else max(0, 100 - penalty)

    # 4 DAX Quality
    dax_items = [(m["Measure Name"], m["Measure Expression"]) for m in measures]
    calc_cols = [c for c in columns if c["Column Type"] == "Calculated"]
    for c in calc_cols:
        dax_items.append((c["Column Name"], ""))
    total_dax = len(dax_items) if dax_items else 1
    ap_clean = sum(1 for _, e in dax_items if not detect_antipatterns(e))
    cx_clean = sum(1 for _, e in dax_items if not detect_complexity(e))
    antipattern_score = ap_clean / total_dax * 100
    complexity_score = cx_clean / total_dax * 100
    fmt_good = sum(1 for m in measures if str(m["Format String"]).strip() != "")
    fmt_score = fmt_good / max(meas_total, 1) * 100
    calc_col_score = ((cols_total - len(calc_cols)) / cols_total * 100) if cols_total else 100
    dax_score = (antipattern_score + complexity_score + fmt_score + calc_col_score) / 4

    # 5 Column Metadata
    cols_with_type = sum(1 for c in columns if c["Data Type"])
    id_total = hidden_id = 0
    for c in columns:
        if re.search(r'(id|key|sk|fk)$', c["Column Name"], re.IGNORECASE):
            id_total += 1
            if c["Is Hidden"]:
                hidden_id += 1
    type_pct = cols_with_type / max(cols_total, 1) * 100
    hidden_pct = (hidden_id / id_total * 100) if id_total > 0 else 100
    col_meta = type_pct * 0.6 + hidden_pct * 0.4

    # 6 Model Structure
    classes = [classify_table(t["Name"]) for t in tables]
    other = sum(1 for v in classes if v == "Other")
    structure = (len(tables) - other) / max(len(tables), 1) * 100

    # 7 Relationship Coverage
    ratio = len(rels) / max(len(tables) - 1, 1)
    rel_cov = min(100, ratio * 100)

    cats = [
        ("Description Coverage", desc_score),
        ("Naming Quality", naming_score),
        ("Relationship Health", rel_health),
        ("DAX Quality", dax_score),
        ("Column Metadata", col_meta),
        ("Model Structure", structure),
        ("Relationship Coverage", rel_cov),
    ]
    overall = round(sum(s for _, s in cats) / len(cats), 1)
    return cats, overall


def grade(o):
    return 'A' if o >= 90 else 'B' if o >= 80 else 'C' if o >= 70 else 'D' if o >= 60 else 'F'


if __name__ == "__main__":
    before = os.path.join(ROOT, "sample-model", "before", "ContosoRetailMini.SemanticModel", "definition")
    after = os.path.join(ROOT, "sample-model", "after", "ContosoRetailMini.SemanticModel", "definition")
    bcats, bo = score(before)
    acats, ao = score(after)
    print(f"{'Category':<24}{'Before':>9}{'After':>9}")
    print("-" * 42)
    for (cb, sb), (ca, sa) in zip(bcats, acats):
        print(f"{cb:<24}{sb:>9.1f}{sa:>9.1f}")
    print("-" * 42)
    print(f"{'OVERALL (avg of 7)':<24}{bo:>9.1f}{ao:>9.1f}")
    print(f"{'GRADE':<24}{grade(bo):>9}{grade(ao):>9}")
