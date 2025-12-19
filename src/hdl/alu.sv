/*
  Fully combinational ALU.
*/

`default_nettype none

module alu (
  input wire clk,

  input alu_func_e alu_func,
  input wire [15:0] a,
  input wire [15:0] b,

  output logic [15:0] out
);
  always_comb begin
    case (alu_func)
      NAND: out = ~(a & b);
      AND: out = a & b;
      NOR: out = ~(a | b);
      OR: out = a | b;
      ADD: out = a + b;
      SUB: out = a - b;
      XOR: out = a ^ b;
      SL: out = a << b[4:0];
      SR: out = a >> b[4:0];
    endcase
  end
endmodule

`default_nettype wire
