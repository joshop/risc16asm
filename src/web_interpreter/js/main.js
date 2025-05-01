import { Interpreter } from './interpreter.js';
import { $ } from './dom.js';
import { fmtHex } from './utils.js';

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
    interp.mem.fill(0);
    interp.mem.set(new Uint16Array(fileReader.result));
    console.log(
      `Uploaded new machine code (${fileReader.result.byteLength} B)`
    );

    $('#start-btn').disabled = false;
    interp.pc = 0;
    interp.updateUI();

    const nextFrame = () => {
      for (let i = 0; i < 16; i++) interp.step();
      interp.updateUI();
      requestAnimationFrame(nextFrame);
    };
    nextFrame();
  };
};

const step = () => {
  interp.step();
  if (interp.cycles % 16 === 0) interp.updateUI();

  let log = `cycle ${interp.cycles.toString().padStart(6)} | `;
  log += `pc ${interp.pc.toString().padStart(5)} | `;
  log += `inst=${fmtHex(interp.mem[interp.pc])} | `;
  log += Array.from(interp.regs)
    .map((x) => `[${x.toString().padStart(5)}]`)
    .join(' ');

  $('#logs').value += `${log}\n`;
};
window.step = step;

fileInputEl.addEventListener('change', readMachineCode, false);
