export const $ = document.querySelector.bind(document);

export const memCanvasCtx = $('#mem-canvas').getContext('2d');

// Memory canvas is 1024 x 1024 x 4
export const memCanvasImageBuffer = new Uint8ClampedArray(1024 * 1024 * 4);
