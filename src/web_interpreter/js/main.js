import { Interpreter } from './interpreter.js';
import { Display } from './display.js';
import { $ } from './dom.js';
import { fmtHex } from './utils.js';

// New display
const display = new Display();
window.display = display;

// New interpreter
const interp = new Interpreter(display);
window.interp = interp;

// Listen for file upload and change system mem
const fileInputEl = $('#file-input');
const fileReader = new FileReader();

// Method to read from file input element
const readMachineCode = () => {
  fileReader.readAsArrayBuffer(fileInputEl.files[0]);
  fileReader.onload = () => {
    interp.mem.fill(0);
    interp.mem.set(new Uint16Array(fileReader.result));
    console.log(
      `Uploaded new machine code (${fileReader.result.byteLength} B)`
    );

    $('#start-btn').disabled = false;
    interp.pc = 0;
    interp.updateUI();

    const nextFrame = () => {
      // Prime number so we hit all the states
      for (let i = 0; i < 4093; i++) interp.step();
      interp.updateUI();
      display.render();
      requestAnimationFrame(nextFrame);
    };
    nextFrame();
  };
};

const step = () => {
  interp.step();
};
window.step = step;

fileInputEl.addEventListener('change', readMachineCode, false);
