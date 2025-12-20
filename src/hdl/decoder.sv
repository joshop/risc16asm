`default_nettype none

module decoder (
  input wire [15:0] inst,

  output logic [2:0] src1,
  output logic [2:0] src2,
  output logic [2:0] dst,
  output logic rf_wen,
  output logic mem_wen
);

endmodule

`default_nettype wire
