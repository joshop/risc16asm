"""
interpreter.py

Takes in memory and executes it.
"""


class RegFile:
    def __init__(self):
        self.regs = [0] * 8

    def get(self, reg_idx: int):
        assert 0 <= reg_idx < 8, f"RegFile.get: reg_idx {reg_idx} not between 0 and 7"
        if reg_idx == 0:
            return 0

        return self.regs[reg_idx]

    def set(self, reg_idx: int, value: int):
        assert 0 <= reg_idx < 8, f"RegFile.set: reg_idx {reg_idx} not between 0 and 7"
        if reg_idx == 0:
            return

        assert 0 <= value < (1 << 16), f"RegFile.set: value {value} not in range"
        self.regs[reg_idx] = value


def execute(mem: list[int]):
    assert len(mem) == (1 << 16), "execute: memory must be of size 1<<16"
