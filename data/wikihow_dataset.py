#!/usr/bin/env python3
import os
import pandas as pd
import jsonlines
from huggingface_hub import hf_hub_download

# ─────────── Directories ───────────
RAW_DIR  = "data/raw"
PROC_DIR = "data/processed"
os.makedirs(RAW_DIR, exist_ok=True)
os.makedirs(PROC_DIR, exist_ok=True)

# ─────────── Download from HF ───────────
print("⏬ Downloading WikiHow-Final.json from HuggingFace…")
hf_file = hf_hub_download(
    repo_id="ajibawa-2023/WikiHow",
    filename="WikiHow-Final.json",
    repo_type="dataset"
)
print(f"✅ Downloaded to {hf_file}")

# ─────────── Load into pandas ───────────
print("📊 Loading into pandas DataFrame…")
# note: this file is JSON lines
df = pd.read_json(hf_file, lines=True)
print("ℹ️  Columns in dataset:", list(df.columns))

# ─────────── Normalize records ───────────
def make_record(row: pd.Series) -> dict:
    # Try common field names; adjust if your JSON uses different keys
    title = row.get("title") or row.get("instruction") or row.get("task") or ""
    steps = row.get("steps") or row.get("text") or row.get("response") or ""
    
    # If 'steps' is a list, join into numbered text
    if isinstance(steps, list):
        output = "\n".join(f"{i+1}. {s}" for i, s in enumerate(steps))
    else:
        output = steps
    
    return {
        "instruction": title,
        "input":       "",
        "output":      output
    }

print("🔄 Converting DataFrame rows to instruction‑output records…")
records = [make_record(r) for _, r in df.iterrows()]
print(f"✅ Prepared {len(records)} records")

# ─────────── Split & Write JSONL ───────────
split_idx = int(len(records) * 0.9)
splits = {
    "train": records[:split_idx],
    "val":   records[split_idx:],
}

for name, recs in splits.items():
    out_path = os.path.join(PROC_DIR, f"wikihow_{name}.jsonl")
    with jsonlines.open(out_path, mode="w") as writer:
        writer.write_all(recs)
    print(f"✍️  Wrote {len(recs)} records to {out_path}")

print("🎉 Done! You now have:")
print(f"  • {PROC_DIR}/wikihow_train.jsonl")
print(f"  • {PROC_DIR}/wikihow_val.jsonl")
