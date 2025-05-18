import { displayCanvasCtx } from './dom.js';

export class Display {
  constructor() {
    this.p = new Uint16Array([0xaaaa, 0xaaaa, 0xaaaa]);
    this.n = new Uint16Array([0xffff, 0xaaaa]);
  }

  // Write to registers
  // addr: 16-bit
  // data: 16-bit
  // Reserved output addresses:
  // 0x4000: col 0
  // 0x4001: col 1
  // 0x4002: col 2
  // 0x4003: row 0
  // 0x4004: row 1

  write(addr, data) {
    if (addr >> 3 !== 0x4000 >> 3) return false;

    console.log(`writing data ${data} to addr ${addr}`);
    if (addr < 0x4003) {
      this.p[addr - 0x4000] = data;
    } else if (addr < 0x4005) {
      this.n[addr - 0x4003] = data;
    } else {
      return false;
    }

    return true;
  }

  render() {
    // Get multiplexed output
    const imageBuffer = new Uint8ClampedArray(48 * 32 * 4);

    for (let row = 0; row < 32; row++) {
      for (let col = 0; col < 48; col++) {
        let pBit = (this.p[col >> 4] >> col % 16) & 1;
        let nBit = (this.n[row >> 4] >> row % 16) & 1;
        let pixelIdx = (row * 48 + col) * 4;

        const c = pBit && !nBit ? 255 : 0;
        imageBuffer[pixelIdx] = c;
        imageBuffer[pixelIdx + 1] = c;
        imageBuffer[pixelIdx + 2] = c;
        imageBuffer[pixelIdx + 3] = 255;
      }
    }

    const iData = new ImageData(imageBuffer, 48, 32);
    displayCanvasCtx.putImageData(iData, 0, 0);
  }
}
