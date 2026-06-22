module decoder (
  input wire clk,
  input wire rst,

  input wire[7:0] inst,         // encoded instruction
  input wire phi,               // phase (0/1)

  // PC control signals
  output logic pc_step_en,      // whether PC <- PC+1

  // Data bus control signals
  output logic adh_to_db_en,
  output logic adh_from_db_en,
  output logic adl_to_db_en,
  output logic adl_from_db_en,
  output logic a_to_db_en,
  output logic a_from_db_en,
  output logic mem_rdata_to_db_en,
  output logic mem_wdata_from_db_en,
  output logic ir_from_db_en,
  output logic alu_to_db_en,

  // Address bus control signals
  output logic ad_to_ab_en,     // address reg -> address bus
  output logic pc_to_ab_en,     // PC to AB
  output logic pc_from_ab_en,   // PC from AB

  // ALU control signals
  output logic [1:0] alu_op,
  output logic alu_cin_sel,     // what ALU C_in is (0 or C)
  output logic c_wen,           // C is write-enable
  output logic [1:0] c_sel      // C <- 1, 0, or ALU out
);

endmodule
