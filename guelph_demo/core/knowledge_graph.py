# Knowledge graph for the Python curriculum.
# Nodes are concepts, directed edges run prerequisite → dependent.

from typing import Dict, List, Optional

import networkx as nx

from core.course_data import CONCEPTS, PREREQUISITE_EDGES


class CurriculumGraph:

    def __init__(self):
        self.graph = nx.DiGraph()
        self._build()

    def _build(self):
        for concept in CONCEPTS:
            self.graph.add_node(concept, description=CONCEPT_DESCRIPTIONS.get(concept, ""))
        for src, dst in PREREQUISITE_EDGES:
            self.graph.add_edge(src, dst)

    def prerequisites_of(self, concept: str) -> List[str]:
        return list(nx.ancestors(self.graph, concept))

    def get_learning_path(self, goal: str, mastery_dict: Dict[str, float], threshold: float = 0.70) -> List[str]:
        """Return ordered unmastered concepts needed to reach the goal."""
        if goal not in self.graph:
            return [goal]

        ancestors = list(nx.ancestors(self.graph, goal))
        try:
            ordered = list(nx.topological_sort(self.graph.subgraph(ancestors + [goal])))
        except nx.NetworkXUnfeasible:
            ordered = ancestors + [goal]

        unmastered = [c for c in ordered if mastery_dict.get(c, 0.0) < threshold]
        return unmastered if unmastered else [goal]

    def _node_colors(self, node, mastery_dict, highlight_path):
        m = mastery_dict.get(node, 0.0)
        if node in highlight_path:
            return "#2980b9", "#5dade2"
        elif m >= 0.70:
            return "#1e8449", "#2ecc71"
        elif m >= 0.40:
            return "#9a6700", "#f39c12"
        return "#7b241c", "#e74c3c"

    def render_dot(self, mastery_dict: Optional[Dict] = None, highlight_path: Optional[List] = None) -> str:
        """Return a Graphviz DOT string for use with st.graphviz_chart."""
        mastery_dict = mastery_dict or {}
        highlight_path = set(highlight_path or [])

        lines = [
            "digraph curriculum {",
            '  graph [bgcolor="#0e1117" rankdir=LR nodesep=0.65 ranksep=1.3]',
            '  node [style="filled,rounded" fontname="Arial" fontsize=11 fontcolor=white shape=box margin="0.22,0.12" penwidth=2]',
            '  edge [arrowsize=0.75 color="#4b5563"]',
            "",
        ]

        for node in self.graph.nodes:
            m = mastery_dict.get(node, 0.0)
            fill, border = self._node_colors(node, mastery_dict, highlight_path)
            lines.append(f'  "{node}" [label="{node}\\n{int(m * 100)}%" fillcolor="{fill}" color="{border}"]')

        lines.append("")

        for src, dst in self.graph.edges:
            on_path = src in highlight_path and dst in highlight_path
            extra = ' [color="#f39c12" penwidth=2.5]' if on_path else ""
            lines.append(f'  "{src}" -> "{dst}"{extra}')

        lines.append("}")
        return "\n".join(lines)

