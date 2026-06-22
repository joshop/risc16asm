module cocotb_iverilog_dump();
initial begin
    $dumpfile("/home/willi/coding/ee/risc16asm/src/hdl_sim/sim_build/alu.fst");
    $dumpvars(0, alu);
end
endmodule
