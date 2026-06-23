from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_GRAPH = ROOT / "reports" / "2026q2-spv-counterparty.graph.json"


def load_graph(path: Path = DEFAULT_GRAPH) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def rank_edges(graph: dict[str, object]) -> list[dict[str, object]]:
    edges = list(graph.get("edges", []))  # type: ignore[arg-type]
    return sorted(edges, key=lambda e: e.get("commitment_amount", 0.0), reverse=True)


def counterparty_exposure(graph: dict[str, object]) -> list[tuple[str, float]]:
    """Total inbound commitment by receiving entity (the concentration view)."""
    totals: dict[str, float] = {}
    for edge in graph.get("edges", []):  # type: ignore[union-attr]
        target = str(edge.get("target", "?"))
        totals[target] = totals.get(target, 0.0) + float(edge.get("commitment_amount", 0.0))
    return sorted(totals.items(), key=lambda kv: kv[1], reverse=True)


def _fmt_usd(amount: float) -> str:
    if amount >= 1e9:
        return f"${amount / 1e9:.2f}B"
    if amount >= 1e6:
        return f"${amount / 1e6:.0f}M"
    return f"${amount:,.0f}"


def render_show(path: Path = DEFAULT_GRAPH) -> str:
    graph = load_graph(path)
    edges = rank_edges(graph)
    nodes = list(graph.get("nodes", []))  # type: ignore[arg-type]
    spvs = [n for n in nodes if n.get("kind") == "spv"]
    sponsors = [n for n in nodes if n.get("kind") == "sponsor"]
    total = sum(float(e.get("commitment_amount", 0.0)) for e in edges)

    lines: list[str] = []
    lines.append("channel-atlas - AI-infra SPV financing graph (2026q2)")
    lines.append("")
    lines.append(
        f"{len(nodes)} entities | {len(spvs)} SPVs | {len(sponsors)} sponsors | "
        f"{len(edges)} financing edges | {_fmt_usd(total)} disclosed"
    )
    lines.append("")

    # ranked edges table
    lines.append("financing edges, ranked by commitment:")
    lines.append("")
    header = f"  {'#':>2}  {'amount':>9}  {'type':<20}  flow"
    lines.append(header)
    lines.append(f"  {'-' * 2}  {'-' * 9}  {'-' * 20}  {'-' * 40}")
    for i, edge in enumerate(edges, 1):
        amt = _fmt_usd(float(edge.get("commitment_amount", 0.0)))
        rel = str(edge.get("relationship_type", "?"))
        flow = f"{edge.get('source', '?')} -> {edge.get('target', '?')}"
        lines.append(f"  {i:>2}  {amt:>9}  {rel:<20}  {flow}")
    lines.append("")

    # concentration view
    exposure = counterparty_exposure(graph)
    lines.append("inbound exposure, ranked by receiving entity:")
    lines.append("")
    for name, amt in exposure:
        lines.append(f"  {_fmt_usd(amt):>9}  {name}")
    lines.append("")

    # headline finding
    if exposure:
        top_name, top_amt = exposure[0]
        share = (top_amt / total * 100) if total else 0.0
        lines.append(
            f"headline: {top_name} is the single largest financing sink at "
            f"{_fmt_usd(top_amt)} ({share:.0f}% of disclosed commitments). "
            "every edge cites a source filing."
        )
    return "\n".join(lines)
