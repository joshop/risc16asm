import { $, memCanvasCtx } from './dom.js';

export class Interpreter {
  constructor() {
    this.mem = new Uint16Array(1 << 16);
    this.pc = 0;
    this.regs = new Uint16Array(8);
  }

  // Registers
  regRead(rs) {
    if (rs === 0) return 0;
    return this.regs[rs];
  }
  regWrite(rd, value) {
    if (rd === 0) return;
    this.regs[rd] = value & 0xffff;
  }

  // Meat of the thing
  execute() {
    const inst = self.mem[self.pc];

    const rs = (inst >> 8) & 0b111;
    const rd = (inst >> 5) & 0b111;
    const ro = (inst >> 2) & 0b111;

    const opImm = (inst >> 14) & 0b11;
    const op5 = (inst >> 11) & 0b11111;
    const op2 = inst & 0b11;
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
    $('#inst').innerText = `h'${this.mem[this.pc].toString(16)}`;
  }
}
