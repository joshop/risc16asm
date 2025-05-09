import { displayCanvasCtx } from './dom.js';

export class Display {
  constructor(interp) {
    //
    this.p = new Uint16Array([0xffff, 0, 1, 4]);
    this.n = new Uint16Array([0, 1, 1, 0xf0f0]);

    this.interp = interp;
  }

  render() {
    // Get multiplexed output
    const imageBuffer = new Uint8ClampedArray(64 * 64 * 4);

    for (let row = 0; row < 64; row++) {
      for (let col = 0; col < 64; col++) {
        let pBit = (this.p[row >> 4] >> row % 16) & 1;
        let nBit = (this.n[col >> 4] >> col % 16) & 1;
        let pixelIdx = (row * 64 + col) * 4;

        const c = pBit && !nBit ? 255 : 0;
        imageBuffer[pixelIdx] = c;
        imageBuffer[pixelIdx + 1] = c;
        imageBuffer[pixelIdx + 2] = c;
        imageBuffer[pixelIdx + 3] = 255;
      }
    }

    const iData = new ImageData(imageBuffer, 64, 64);
    displayCanvasCtx.putImageData(iData, 0, 0);
  }
}
