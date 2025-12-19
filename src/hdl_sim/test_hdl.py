import os
import sys
import glob
import random
from tqdm import tqdm

from pathlib import Path

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import Timer, ClockCycles
from cocotb.runner import get_runner

sys.path.append(Path(__file__).resolve().parent.parent._str)

proj_path = Path(__file__).resolve().parent.parent.parent
test_file = os.path.basename(__file__).replace(".py", "")

HDL_TOPLEVEL = "alu"

@cocotb.test()
async def test_module(dut):
    """cocotb test for the lazy mult module"""
    dut._log.info("Starting...")
    cocotb.start_soon(Clock(dut.clk, 10, units="ns").start())

    testcases = [
        (0, lambda a, b: ~(a & b)),                 # NAND
        (1, lambda a, b: (a & b)),                  # AND
        (2, lambda a, b: ~(a | b)),                 # NOR
        (3, lambda a, b: (a | b)),                  # OR
        (4, lambda a, b: (a + b)),                  # ADD
        (5, lambda a, b: (a - b)),                  # SUB
        (6, lambda a, b: (a ^ b)),                  # XOR
        (7, lambda a, b: (a << (b & 0b11111))),     # SL
        (8, lambda a, b: (a >> (b & 0b11111))),     # SR
    ]

    # Test each operation in turn
    for alu_func, test_func in testcases:
        dut.alu_func.value = alu_func

        for a in tqdm(
            random.sample(range(2**16), k=100), ncols=80,
            desc=f"alu_func={alu_func+1}/{len(testcases)}"
        ):
            for b in random.sample(range(2**16), k=100):
                dut.a.value = a
                dut.b.value = b
                await Timer(10, "ns")

                exp_ans = test_func(a, b) & 0xFFFF
                if dut.out.value != exp_ans:
                    raise ValueError(
                        f"Wrong answer on {alu_func=}, {a=}, {b=}. Expected {exp_ans}, got {dut.out.value}")


def runner():
    """Module tester."""
    
    sim = os.getenv("SIM", "icarus")
    # sys.path.append(str(proj_path / "sim" / "model"))

    sources = [
        *glob.glob(str(proj_path / "src" / "hdl" / "*.sv"))
    ]
    build_test_args = ["-Wall"]

    # values for parameters defined earlier in the code.
    parameters = {}

    # sys.path.append(str(proj_path / "sim"))
    hdl_toplevel = "alu"
    
    runner = get_runner(sim)
    runner.build(
        sources=sources,
        hdl_toplevel=hdl_toplevel,
        always=True,
        build_args=build_test_args,
        parameters=parameters,
        timescale=("1ns", "1ps"),
        waves=True,
        build_dir=(proj_path / "src" / "hdl_sim" / "sim_build")
    )
    run_test_args = []
    runner.test(
        hdl_toplevel=hdl_toplevel,
        test_module=test_file,
        test_args=run_test_args,
        waves=True,
    )


if __name__ == "__main__":
    runner()
