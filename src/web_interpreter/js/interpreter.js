import { $, memCanvasCtx } from './dom.js';
import { parseImm, fmtHex } from './utils.js';

// Instruction type constants (mimicking enums)
// IMM instruction types (inst[15:14])
const ADDI = 0b10;
const NANDI = 0b11;

// Regular instruction types (inst[15:11])
const LUI = 0b01000;
const LOGICAL = 0b01001;
const ADDSUB = 0b01100;
const SHIFT = 0b01010;
const XOR = 0b01101;
const JUMP = 0b00000;
const BR_BZ = 0b00100;
const BR_BNZ = 0b00101;
const BR_BP = 0b00110;
const BR_BNP = 0b00111;
const LOAD = 0b00010;
const STORE = 0b00011;

export class Interpreter {
  constructor() {
    this.mem = new Uint16Array(1 << 16);
    this.pc = 0;
    this.regs = new Uint16Array(8);
    this.cycles = 0;
  }

  // Registers
  rfr(rs) {
    if (rs === 0) return 0;
    return this.regs[rs];
  }
  rfw(rd, value) {
    if (rd === 0) return;
    this.regs[rd] = value & 0xffff;
  }

  // Meat of the thing
  step() {
    this.cycles++;

    const inst = this.mem[this.pc];
    let nextPc = (this.pc + 1) & 0xffff; // Default next pc

    // Extract instruction fields
    const rs = (inst >> 8) & 0b111;
    const rd = (inst >> 5) & 0b111;
    const ro = (inst >> 2) & 0b111;

    // Extract opcode types
    const opImm = (inst >> 14) & 0b11;
    const op5 = (inst >> 11) & 0b11111;
    const op2 = inst & 0b11;

    // Extract immediate values
    const immImm = parseImm(
      ((inst & (0b111 << 11)) >> 6) + (inst & 0b11111),
      8
    );
    const immLui = parseImm(((inst & (0b111 << 8)) >> 3) + (inst & 0b11111), 8);
    const immBr = parseImm(inst & 0b11111111, 8);
    const immLoad = parseImm(inst & 0b11111, 5);
    const immStore = parseImm(((inst & (0b111 << 5)) >> 3) + (inst & 0b11), 5);

    // IMM-TYPE instructions
    if (opImm === ADDI || opImm === NANDI) {
      if (opImm === ADDI) {
        // addi
        console.log(`addi rd=${rd}`);
        this.rfw(rd, (this.rfr(rs) + immImm) & 0xffff);
      } else if (opImm === NANDI) {
        // nandi
        this.rfw(rd, ~(this.rfr(rs) & immImm) & 0xffff);
      }
      this.pc = nextPc;
      return;
    }

    // Handle other instruction types
    switch (op5) {
      case LUI:
        this.rfw(rd, (immLui << 8) & 0xffff);
        break;

      case LOGICAL:
        switch (op2) {
          case 0b00:
            this.rfw(rd, ~(this.rfr(rs) & this.rfr(ro)) & 0xffff);
            break;
          case 0b01:
            this.rfw(rd, this.rfr(rs) & this.rfr(ro));
            break;
          case 0b11:
            this.rfw(rd, ~(this.rfr(rs) | this.rfr(ro)) & 0xffff);
            break;
          case 0b10:
            this.rfw(rd, this.rfr(rs) | this.rfr(ro));
            break;
        }
        break;

      case ADDSUB:
        switch (op2) {
          case 0b00:
          case 0b01:
            this.rfw(rd, (this.rfr(rs) + this.rfr(ro)) & 0xffff);
            break;
          case 0b10:
          case 0b11:
            this.rfw(rd, (this.rfr(rs) - this.rfr(ro)) & 0xffff);
            break;
        }
        break;

      case XOR:
        this.rfw(rd, this.rfr(rs) ^ this.rfr(ro));
        break;

      case SHIFT:
        const shamt = inst & 0b1111;
        const sd = (inst & (0b1 << 4)) >> 4;
        if (sd === 0) {
          this.rfw(rd, this.rfr(rs) << shamt);
        } else {
          this.rfw(rd, this.rfr(rs) >> shamt);
        }
        break;

      case JUMP:
        nextPc = this.rfr(rs);
        this.rfw(rd, this.pc + 1);
        break;

      case BR_BZ:
        if (this.rfr(rs) === 0) {
          nextPc = this.pc + immBr;
        }
        break;

      case BR_BNZ:
        if (this.rfr(rs) !== 0) {
          nextPc = this.pc + immBr;
        }
        break;

      case BR_BP:
        if (!(this.rfr(rs) & (1 << 15))) {
          nextPc = this.pc + immBr;
        }
        break;

      case BR_BNP:
        if (this.rfr(rs) & (1 << 15)) {
          nextPc = this.pc + immBr;
        }
        break;

      case LOAD:
        this.rfw(rd, this.mem[this.rfr(rs) + immLoad]);
        break;

      case STORE:
        console.log(
          `writing to index ${this.rfr(rs) + immStore}, value ${
            this.rfr(ro) & 0xffff
          }`
        );
        this.mem[this.rfr(rs) + immStore] = this.rfr(ro) & 0xffff;
        break;
    }

    this.pc = nextPc;
  }

  // UI refresh!
  updateUI() {
    // Refresh canvas
    const imageBuffer = new Uint8ClampedArray((1 << 16) * 16 * 4);
    for (let wordIdx = 0; wordIdx < 1 << 16; wordIdx++) {
      for (let bitIdx = 0; bitIdx < 16; bitIdx++) {
        let bit = (this.mem[wordIdx] >> bitIdx) & 1;
        let pixelIdx = (wordIdx * 16 + bitIdx) * 4;

        const c = bit ? 255 : 0;
        imageBuffer[pixelIdx] = c;
        imageBuffer[pixelIdx + 1] = c;
        imageBuffer[pixelIdx + 2] = c;
        imageBuffer[pixelIdx + 3] = 255;
      }
    }
    const iData = new ImageData(imageBuffer, 1024, 1024);
    memCanvasCtx.putImageData(iData, 0, 0);

    // Update PC
    $('#pc').innerText = this.pc;
    $('#inst').innerText = fmtHex(this.mem[this.pc]);
    $('#cycle').innerText = this.cycles;

    for (let i = 1; i <= 7; i++) {
      // $(`#r${i}`).innerText = fmtHex(this.rfr(i));
      $(`#r${i}`).innerText = this.rfr(i).toString().padStart(5);
    }
  }
}
