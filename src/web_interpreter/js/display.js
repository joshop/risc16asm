import { displayCanvasCtx } from './dom.js';

export class Display {
  constructor() {
    this.p = new Uint16Array([0xaaaa, 0xaaaa, 0xaaaa]);
    this.n = new Uint16Array([0xffff, 0xaaaa]);

    this.pixelHistory = [];
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
  // Return true if they were modified

  write(addr, data) {
    if (addr >> 3 !== 0x4000 >> 3) return false;

    if (addr < 0x4003) {
      this.p[addr - 0x4000] = data;
    } else if (addr < 0x4005) {
      this.n[addr - 0x4003] = data;
    } else {
      return false;
    }

    // Calculate pixels, add to history
    let pixels = this.getPixels();
    this.pixelHistory.push(pixels);

    return true;
  }

  getPixels() {
    // Calculate pixel values
    const pixels = new Uint8Array(48 * 32);
    for (let row = 0; row < 32; row++) {
      for (let col = 0; col < 48; col++) {
        let pBit = (this.p[col >> 4] >> col % 16) & 1;
        let nBit = (this.n[row >> 4] >> row % 16) & 1;
        let pixelIdx = row * 48 + col;

        const on = pBit && !nBit;
        pixels[pixelIdx] = on;
      }
    }
    return pixels;
  }

  render() {
    // Calculate average pixel values since last render
    const imageBuffer = new Uint8ClampedArray(48 * 32 * 4);
    const n = this.pixelHistory.length;
    if (n === 0) return;

    for (let pixelIdx = 0; pixelIdx < 48 * 32; pixelIdx++) {
      let brightnessSum = 0;
      for (let i = 0; i < n; i++) {
        brightnessSum += this.pixelHistory[i][pixelIdx];
      }

      let c = Math.floor((1 - (brightnessSum / n) * 48) * 255);
      imageBuffer[pixelIdx * 4 + 0] = c;
      imageBuffer[pixelIdx * 4 + 1] = c;
      imageBuffer[pixelIdx * 4 + 2] = c;
      imageBuffer[pixelIdx * 4 + 3] = 255;
    }

    const iData = new ImageData(imageBuffer, 48, 32);
    displayCanvasCtx.putImageData(iData, 0, 0);

    this.pixelHistory = [];
  }
}
