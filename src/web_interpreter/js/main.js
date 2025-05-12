import { Interpreter } from './interpreter.js';
import { Display } from './display.js';
import { $ } from './dom.js';
import { fmtHex } from './utils.js';

// New interpreter
const interp = new Interpreter();
window.interp = interp;

// New display
const display = new Display(interp);
window.display = display;

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
      for (let i = 0; i < 1; i++) interp.step();
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
