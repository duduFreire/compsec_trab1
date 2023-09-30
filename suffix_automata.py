
class SuffixAutomata:
    @dataclass
    class State:
        size: int
        to: dict[str, int]
        link: int
        first_occur: int
        back_link: list[int]

    def __init__(self, text: str) -> None:
        self._build(text)
        self.lastID = 1
        self.last = 1
        self.states = []

    def _build(self, text: str) -> None:
        for c in text:
            self._push(c)

    def _push(self, c: str) -> None:
        a = self._next_id()
        b = self.last
        self.states[a].size = self.states[b].size + 1
        self.last = a
        self.states[a].first_occur = self.states[a].size - 1
        
        while b > 0 and not self.states[b].to[c]:
            self.states[b].to[c] = a
            b = self.states[b].link

        if b == 0:
            self.states[a].link = 1
            self.states[1].back_link.append(a)
            return

        p = self.states[b].to[c]
        if self.states[b].size + 1 == self.states[p].size:
            self.states[a].link = p
            self.states[p].back_link.append(a)
            return

        clone = _clone_states(p)

        self.states[clone].size = self.states[b].size + 1
        self.states[p].link = clone
        self.states[a].link = clone

        self.states[clone].back_link.append(p)
        self.states[clone].back_link.append(p)
        while self.states[b].to[c] == p:
            self.states[b].to[c] = clone
            b = self.states[b].link

    def _next_id(self) -> int:
        self.lastID += 1
        return self.lastID

    def _clone_state(state: int) -> int:
        clone = _next_id()
        for k, v: self.states[state].items():
            self.states[clone].to[k] = v

        self.states[clone].link = self.states[state].link
        self.states[clone].first_pos = self.states[state].firs_pos
        return clone

    def find_all(pattern: str) -> list[int]:
        def _get_pattern_state(state: int, idx: int) -> int:
            if (state == 0):
                return 0
            if idx >= len(pattern):
                return state
            return _get_pattern_state(self.states[state].to[pattern[idx]], idx+1)

        state = _get_pattern_state(1, 0)
        positions = []

        def _get_all_pos(state: int, positions) -> None:
            positions.apped(self.states[state].first_pos)
            for b in self.states[state].back_link:
                get_all_pos(b, positions)

        return positions


