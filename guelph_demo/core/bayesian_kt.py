# Bayesian Knowledge Tracing — 4-parameter model (Corbett & Anderson, 1995)
#
# L0  prior probability the student already knows the concept
# T   probability of learning after one attempt
# G   guess rate (correct answer without knowing)
# S   slip rate  (wrong answer despite knowing)
#
# Update equations:
#   correct:   P(L|obs) = L*(1-S) / [L*(1-S) + (1-L)*G]
#   incorrect: P(L|obs) = L*S     / [L*S + (1-L)*(1-G)]
#   then:      L_new    = P(L|obs) + (1 - P(L|obs)) * T

from typing import Dict
import numpy as np


class BKTModel:
    """Tracks per-concept mastery and updates it after each quiz answer."""

    def __init__(self, params: Dict[str, Dict[str, float]]):
        self._params = params
        self._mastery = {c: p["L0"] for c, p in params.items()}

    def update(self, concept: str, correct: bool) -> float:
        """Run one BKT update and return the new mastery estimate."""
        if concept not in self._params:
            raise KeyError(f"Unknown concept: {concept!r}")

        p = self._params[concept]
        L = self._mastery[concept]
        T, G, S = p["T"], p["G"], p["S"]

        # Bayesian posterior given the observed answer
        if correct:
            posterior = (L * (1 - S)) / (L * (1 - S) + (1 - L) * G)
        else:
            posterior = (L * S) / (L * S + (1 - L) * (1 - G))

        # Apply learning rate
        new_mastery = posterior + (1 - posterior) * T
        self._mastery[concept] = float(np.clip(new_mastery, 0.0, 1.0))
        return self._mastery[concept]

    def mastery(self, concept: str) -> float:
        return self._mastery.get(concept, 0.0)

    def all_mastery(self) -> Dict[str, float]:
        return dict(self._mastery)

    def reset(self) -> None:
        for concept, p in self._params.items():
            self._mastery[concept] = p["L0"]

    def mastery_label(self, concept: str) -> str:
        m = self.mastery(concept)
        if m >= 0.70:
            return "Mastered"
        elif m >= 0.40:
            return "In Progress"
        return "Not Started"

    def mastery_color(self, concept: str) -> str:
        m = self.mastery(concept)
        if m >= 0.70:
            return "#2ecc71"
        elif m >= 0.40:
            return "#f39c12"
        return "#e74c3c"
