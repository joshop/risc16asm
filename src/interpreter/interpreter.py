import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils import format_const as fmt
from interpreter.reg_file import RegFile
from interpreter.execute import execute


class Interpreter:
    def __init__(self):
        """
        Creates a new interpreter that executes an assembled binary file.
        """
        self.mem = [0] * (1 << 16)
        self.rf = RegFile()
        self.pc = 0
        self.cycles = 0

    def is_halted(self):
        """
        Determines whether the current instruction is bz r0, <zero offset>
        """
        return self.mem[self.pc] == 0b00100_000_00000000

    def dump_state(self, base=10):
        """
        Return a formatted string containing pc and contents of registers.
            base: 2, 10, or 16 (base to display in)
        """
        reg_str = " ".join([f"[{fmt(self.rf[i], base)}]" for i in range(8)])
        return (
            f"pc={fmt(self.pc, base)} | inst={fmt(self.mem[self.pc], 16)} | {reg_str}"
        )

    def load_program(self, prog: bytes | str):
        """
        Load machine code into the program.
            prog: a sequence of bytes, or filename
        """
        if isinstance(prog, str):
            with open(prog, "rb") as fin:
                prog = fin.read()

        assert isinstance(prog, bytes), f"Expected bytes for prog, got {type(prog)}"
        assert len(prog) % 2 == 0, f"Expected even number of bytes, got {len(prog)}"

        for byte_idx in range(0, len(prog), 2):
            word = int.from_bytes(prog[byte_idx : byte_idx + 2], "little")
            self.mem[byte_idx // 2] = word

    def step(self):
        """
        Execute the instruction at mem[pc] and advance pc
        """
        next_pc = execute(self.pc, self.rf, self.mem)
        self.pc = next_pc
        self.cycles += 1
