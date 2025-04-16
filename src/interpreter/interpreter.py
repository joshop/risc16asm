from reg_file import RegFile
from execute import execute


class Interpreter:
    def __init__(self):
        """
        Creates a new interpreter that executes an assembled binary file.
        """
        self.mem = [0] * (1 << 16)
        self.rf = RegFile()
        self.pc = 0

    def dump_state(self):
        reg_str = ", ".join([f"r{i}=0x{self.rf[i]:04x}" for i in range(8)])
        return f"pc=0x{self.pc:04x} {reg_str}"

    def load_program(self, prog: bytes | str):
        """
        Load machine code into the program.
            prog: a sequence of an even number of bytes, or filename
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
        next_pc = execute(self.pc, self.rf, self.mem)
        self.pc = next_pc


if __name__ == "__main__":
    interp = Interpreter()
    interp.load_program("./scripts/test_1.bin")

    while True:
        interp.step()
        print(interp.dump_state())
