// Tristate buffer

`default_nettype none

module tristate_buffer #(
  parameter integer WIDTH = 16
) (
  input wire en,
  input wire [WIDTH-1:0] d,
  output wire [WIDTH-1:0] y
);
  assign y = en ? d : {(WIDTH){1'bz}};;
endmodule

`default_nettype wire
