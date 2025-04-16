class RegFile:
    def __init__(self):
        """
        Create a new register file class instance.
          - Writing to 0 register does nothing
          - Reading from 0 register always returns 0
          - Set values are anded with 0xFFFF to ensure it fits in 16 bits
        """
        self.regs = [0] * 8

    def __getitem__(self, key):
        return self.get(key)

    def __setitem__(self, key, value):
        return self.set(key, value)

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
        self.regs[reg_idx] = value & 0xFFFF
