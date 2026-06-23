typedef enum {
  OP_LI,
  OP_ADD, OP_ADDC, OP_NAND,
  OP_CLRC, OP_SETC,
  OP_TAL, OP_TAH, OP_TLA, OP_THA,
  OP_STA, OP_LDA,
  OP_JMP, OP_JZ, OP_JNZ
} inst_type_t;

module decoder (
  input wire [7:0] inst,        // encoded instruction
  input wire phi,               // phase (0/1)
  input wire a_zero,            // whether A == 0

  // Control flow
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
  always_comb begin
    if (~phi) begin
      // Copy mem data to IR
      ad_to_ab_en = 1'b1;
      mem_rdata_to_db_en = 1'b1;
      ir_from_db_en = 1'b1;

      pc_step_en = 1'b1;
      
    end else begin
      // First four bits of `inst` carry data
      // We may modify this later
      // Default zero for everything

      case (inst[3:0])
        // LI
        4'b0001: begin
          pc_to_ab_en = 1'b1;
          mem_rdata_to_db_en = 1'b1;
          a_from_db_en = 1'b1;
          pc_step_en = 1b'1;
        end
        4'b0010: begin
          // continue...
        end
      endcase
    end
  end

endmodule
