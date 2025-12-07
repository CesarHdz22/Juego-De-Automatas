# automata/dfa.py
from dataclasses import dataclass, field
from typing import Dict, Set, Tuple

@dataclass(frozen=True)
class State:
    name: str

@dataclass
class DFA:
    alphabet: Set[str]
    states: Set[State] = field(default_factory=set)
    start: State | None = None
    accept: Set[State] = field(default_factory=set)
    transitions: Dict[Tuple[State, str], State] = field(default_factory=dict)

    def add_state(self, name: str, is_start=False, is_accept=False) -> State:
        s = State(name)
        self.states.add(s)
        if is_start:
            self.start = s
        if is_accept:
            self.accept.add(s)
        return s

    def set_transition(self, from_state: State, symbol: str, to_state: State) -> None:
        if symbol not in self.alphabet:
            raise ValueError(f"Symbol '{symbol}' not in alphabet {self.alphabet}")
        self.transitions[(from_state, symbol)] = to_state

    def run(self, input_str: str) -> bool:
        if not self.start:
            raise RuntimeError("Start state not set.")
        current = self.start
        for ch in input_str:
            if ch not in self.alphabet:
                return False
            key = (current, ch)
            if key not in self.transitions:
                return False
            current = self.transitions[key]
        return current in self.accept