from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parent
GRAPH_PATH = ROOT / "reports" / "2026q2-spv-counterparty.graph.json"


def fmt_usd(amount: float) -> str:
    if amount >= 1e9:
        return f"${amount / 1e9:.2f}B"
    if amount >= 1e6:
        return f"${amount / 1e6:.0f}M"
    return f"${amount:,.0f}"


st.set_page_config(page_title="channel-atlas", layout="wide")
st.title("channel-atlas")
st.caption("AI-infra SPV financing graph (2026q2) - every edge cites a source filing")

if not GRAPH_PATH.is_file():
    st.warning(
        "missing artifact: reports/2026q2-spv-counterparty.graph.json. "
        "run `python -m channel_atlas build` to generate it."
    )
    st.stop()

graph = json.loads(GRAPH_PATH.read_text(encoding="utf-8"))
edges = graph.get("edges", [])
nodes = graph.get("nodes", [])

rows = []
for e in edges:
    filing = (e.get("source_filings") or [{}])[0]
    rows.append(
        {
            "from": e.get("source", "?"),
            "to": e.get("target", "?"),
            "type": e.get("relationship_type", "?"),
            "commitment (USD)": float(e.get("commitment_amount", 0.0)),
            "filing": filing.get("url", ""),
        }
    )
df = pd.DataFrame(rows).sort_values("commitment (USD)", ascending=False).reset_index(drop=True)

total = float(df["commitment (USD)"].sum()) if not df.empty else 0.0
spv_count = sum(1 for n in nodes if n.get("kind") == "spv")

# inbound exposure by receiving entity
exposure = (
    df.groupby("to")["commitment (USD)"].sum().sort_values(ascending=False)
    if not df.empty
    else pd.Series(dtype=float)
)
top_sink = exposure.index[0] if len(exposure) else "n/a"
top_sink_amt = float(exposure.iloc[0]) if len(exposure) else 0.0
top_share = (top_sink_amt / total * 100) if total else 0.0

c1, c2, c3 = st.columns(3)
c1.metric("disclosed commitments", fmt_usd(total))
c2.metric("SPVs / edges", f"{spv_count} / {len(edges)}")
c3.metric("largest sink share", f"{top_share:.0f}%")

st.info(
    f"headline: {top_sink} is the single largest financing sink at "
    f"{fmt_usd(top_sink_amt)} ({top_share:.0f}% of disclosed commitments)."
)

st.subheader("financing edges, ranked by commitment")

relationship_types = sorted(df["type"].unique().tolist()) if not df.empty else []
chosen = st.multiselect(
    "filter by relationship type",
    options=relationship_types,
    default=relationship_types,
)
view = df[df["type"].isin(chosen)] if chosen else df

display = view.copy()
display["commitment"] = display["commitment (USD)"].map(fmt_usd)
st.dataframe(
    display[["from", "to", "type", "commitment", "filing"]],
    use_container_width=True,
    hide_index=True,
    column_config={"filing": st.column_config.LinkColumn("filing")},
)

st.subheader("inbound exposure by receiving entity")
exp_view = exposure.loc[exposure.index.isin(view["to"])] if not view.empty else exposure
st.bar_chart(exp_view)
