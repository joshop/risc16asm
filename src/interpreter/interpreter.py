from .reg_file import RegFile


class Interpreter:
    def __init__(self):
        """
        Creates a new interpreter that executes an assembled binary file.
        """
        self.mem = [0] * (1 << 16)
        self.rf = RegFile()

    def load_program(self, prog: bytes | str):
        """
        Load machine code into the program.
            prog: a sequence of an even number of bytes, or filename
        """
        if isinstance(prog, str):
            pass

        assert isinstance(prog, bytes), f"Expected bytes for prog, got {type(prog)}"
        assert len(prog) % 2 == 0, f"Expected even number of bytes, got {len(prog)}"
        for byte_idx in range(len(prog)):
            word = int.from_bytes(prog[byte_idx : byte_idx + 2], "little")
            self.mem[byte_idx // 2] = word
