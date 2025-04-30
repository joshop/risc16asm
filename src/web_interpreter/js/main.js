import { Interpreter } from './interpreter.js';
import { $ } from './dom.js';

// New interpreter
const interp = new Interpreter();
window.interp = interp;

// Listen for file upload and change system mem
const fileInputEl = $('#file-input');
const fileReader = new FileReader();

// Method to read from file input element
const readMachineCode = () => {
  fileReader.readAsArrayBuffer(fileInputEl.files[0]);
  fileReader.onload = () => {
    interp.mem = new Uint16Array(fileReader.result);
    console.log(
      `Uploaded new machine code (${fileReader.result.byteLength} B)`
    );

    interp.pc = 0;

    interp.updateUI();
  };
};

fileInputEl.addEventListener('change', readMachineCode, false);
