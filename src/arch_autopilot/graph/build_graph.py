from __future__ import annotations

from langgraph.graph import StateGraph, START, END

from .nodes import generate_report_node, prioritize_findings_node


def build_graph():
    g = StateGraph(dict)
    g.add_node("prioritize", prioritize_findings_node)
    g.add_node("report", generate_report_node)

    g.set_entry_point("prioritize")
    g.add_edge("prioritize", "report")
    g.add_edge("report", END)

    return g.compile()


