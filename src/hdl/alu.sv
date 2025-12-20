/*
  Fully combinational ALU
*/

`default_nettype none

// Subcomponents
module alu_adder (
  input wire [15:0] a,
  input wire [15:0] b,
  input wire carry_in,
  output logic [15:0] out
);
  assign out = (a + b + carry_in);
endmodule

module alu_shifter (
  input wire [15:0] a,
  input wire shift_dir,
  output logic [15:0] out
);
  // shit_dir is 0 for left shift, 1 for right shift
  assign out = shift_dir ? (a >> 1) : (a << 1);
endmodule

module alu_nand (
  input wire [15:0] a,
  input wire [15:0] b,
  output wire [15:0] out
);
  assign out = ~(a & b);
endmodule

module alu_xor (
  input wire [15:0] a,
  input wire [15:0] b,
  output wire [15:0] out
);
  assign out = a ^ b;
endmodule

// Actual ALU module
module alu (
  input wire [15:0] a,
  input wire [15:0] b,

  // Control signals
  input wire is_neg_a,
  input wire is_neg_b,
  input wire is_neg_out,

  // More control signals
  input wire is_add_sub,
  input wire is_shift,
  input wire is_nand,
  input wire is_xor,
  input wire shift_dir,

  output logic [15:0] out
);
  logic [15:0] adder_out, shifter_out, nand_out, xor_out;
  wire [15:0] out_preneg;   // Three-state signal
  logic [15:0] neg_a, neg_b;

  assign neg_a = a ^ {(16){is_neg_a}};
  assign neg_b = b ^ {(16){is_neg_b}};

  alu_adder adder (
    .a(a),
    .b(neg_b),
    .carry_in(is_neg_b),
    .out(adder_out)
  );

  alu_shifter shifter (
    .a(a),
    .shift_dir(shift_dir),
    .out(shifter_out)
  );

  alu_nand nander (
    .a(neg_a),
    .b(neg_b),
    .out(nand_out)
  );

  alu_xor xorer (
    .a(a),
    .b(b),
    .out(xor_out)
  );

  tristate_buffer #(16) tsb_adder (.en(is_add_sub), .d(adder_out), .y(out_preneg));
  tristate_buffer #(16) tsb_shifter (.en(is_shift), .d(shifter_out), .y(out_preneg));
  tristate_buffer #(16) tsb_nand (.en(is_nand), .d(nand_out), .y(out_preneg));
  tristate_buffer #(16) tsb_xor (.en(is_xor), .d(xor_out), .y(out_preneg));
  
  assign out = out_preneg ^ {(16){is_neg_out}};
endmodule

`default_nettype wire
