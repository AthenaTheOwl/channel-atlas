from __future__ import annotations

import json
import sys
from pathlib import Path

import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parent
GRAPH_PATH = ROOT / "reports" / "2026q2-spv-counterparty.graph.json"

# make the package importable so we can drive the REAL engine, not a lookup.
sys.path.insert(0, str(ROOT / "src"))
from channel_atlas.graph import build_graph  # noqa: E402
from channel_atlas.models import CounterpartyEdge, SourceFiling, SpvRecord  # noqa: E402
from channel_atlas.show import counterparty_exposure, rank_edges  # noqa: E402


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

# --------------------------------------------------------------------------
# interactive: drive the real engine on your own financing edges
# --------------------------------------------------------------------------
st.divider()
st.subheader("build your own financing graph")
st.caption(
    "this is not a lookup. edit the edges below (change commitments, retype a "
    "relationship, add a new SPV flow) and the app re-runs the real engine "
    "(channel_atlas.graph.build_graph + channel_atlas.show.counterparty_exposure) "
    "to re-rank the concentration view live."
)

# seed the editor from the committed edges so the user starts from a real ledger.
seed = pd.DataFrame(
    [
        {
            "from": e.get("source", "?"),
            "to": e.get("target", "?"),
            "relationship_type": e.get("relationship_type", "?"),
            "commitment_amount": float(e.get("commitment_amount", 0.0)),
        }
        for e in edges
    ]
)

edited = st.data_editor(
    seed,
    num_rows="dynamic",
    use_container_width=True,
    hide_index=True,
    key="edge_editor",
    column_config={
        "from": st.column_config.TextColumn("from (payer)"),
        "to": st.column_config.TextColumn("to (sink)"),
        "relationship_type": st.column_config.TextColumn("type"),
        "commitment_amount": st.column_config.NumberColumn(
            "commitment (USD)", min_value=0.0, step=50_000_000.0, format="%.0f"
        ),
    },
)

# turn the edited rows into the real dataclasses the engine consumes.
placeholder_filing = SourceFiling(url="user-input://draft", accession_number="-", cited_at="-")
user_edges: list[CounterpartyEdge] = []
user_spvs: list[SpvRecord] = []
for i, row in edited.reset_index(drop=True).iterrows():
    frm = str(row.get("from") or "").strip()
    to = str(row.get("to") or "").strip()
    if not frm or not to:
        continue
    user_edges.append(
        CounterpartyEdge(
            edge_id=f"user-edge-{i:03d}",
            from_entity=frm,
            to_entity=to,
            relationship_type=str(row.get("relationship_type") or "unspecified").strip(),
            commitment_amount=float(row.get("commitment_amount") or 0.0),
            commitment_currency="USD",
            disclosure_date="-",
            source_filings=[placeholder_filing],
        )
    )

if not user_edges:
    st.warning("add at least one edge with a from-entity and a to-entity.")
else:
    # CALL THE REAL ENGINE: same build_graph the CLI 'build' verb uses.
    user_graph = build_graph(user_spvs, user_edges)
    ranked = rank_edges(user_graph)
    user_exposure = counterparty_exposure(user_graph)
    user_total = sum(float(e.get("commitment_amount", 0.0)) for e in ranked)

    m1, m2, m3 = st.columns(3)
    m1.metric("your disclosed commitments", fmt_usd(user_total))
    m2.metric("edges", str(len(ranked)))
    if user_exposure:
        top_name, top_amt = user_exposure[0]
        top_pct = (top_amt / user_total * 100) if user_total else 0.0
        m3.metric("largest sink share", f"{top_pct:.0f}%")
        st.info(
            f"recomputed headline: {top_name} is now the single largest financing "
            f"sink at {fmt_usd(top_amt)} ({top_pct:.0f}% of your commitments)."
        )

    st.markdown("**re-ranked inbound exposure (real engine output):**")
    exp_series = pd.Series(
        {name: amt for name, amt in user_exposure}, dtype=float, name="commitment (USD)"
    )
    st.bar_chart(exp_series)

    st.markdown("**your edges, re-ranked by commitment:**")
    ranked_df = pd.DataFrame(
        [
            {
                "from": e.get("source"),
                "to": e.get("target"),
                "type": e.get("relationship_type"),
                "commitment": fmt_usd(float(e.get("commitment_amount", 0.0))),
            }
            for e in ranked
        ]
    )
    st.dataframe(ranked_df, use_container_width=True, hide_index=True)
