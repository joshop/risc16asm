// Registers of various sizes

`default_nettype none

module register #(
  parameter integer WIDTH
) (
  input wire clk,
  input wire rst,

  // Control signals
  input wire we,
  input wire oe,

  input wire [WIDTH-1:0] in,
  output logic [WIDTH-1:0] out
);
  // Internal state
  logic [WIDTH-1:0] q;

  always_ff @(posedge clk) begin
    if (rst) begin
      q <= 0;
    end else if (we) begin
      q <= in;
    end
  end

  // Output is oe-gated
  assign out = oe ? q : 'z;
endmodule

`default_nettype wire
