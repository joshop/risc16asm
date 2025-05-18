import { Interpreter } from './interpreter.js';
import { Display } from './display.js';
import { $ } from './dom.js';

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

    $('#step-btn').disabled = false;
    $('#play-btn').disabled = false;
    $('#pause-btn').disabled = true;
    interp.pc = 0;
    interp.updateUI();
  };
};

// State
let playing = true;
$('#step-btn').disabled = true;
$('#play-btn').disabled = true;
$('#pause-btn').disabled = true;

let lastCycleCount = 0;

// Handler to advance simulation by a bunch and update display
const nextFrame = () => {
  // Prime number so we hit all the states
  let count = 0;
  while (true) {
    const displayUpdated = interp.step();

    // Break once in a while or if display refreshed
    // if (count > 4096) break;
    if (displayUpdated && count > 4096) {
      console.log(interp.cycles - lastCycleCount);
      break;
    }

    count++;
  }
  lastCycleCount = interp.cycles;
  interp.updateUI();
  display.render();

  if (playing) requestAnimationFrame(nextFrame);
};
window.nextFrame = nextFrame;

// Button handlers
const step = () => {
  interp.step();
  interp.updateUI();
  display.render();
};
window.step = step;

const play = () => {
  playing = true;
  nextFrame();
  $('#play-btn').disabled = true;
  $('#pause-btn').disabled = false;
};
window.play = play;

const pause = () => {
  playing = false;
  $('#play-btn').disabled = false;
  $('#pause-btn').disabled = true;
};
window.pause = pause;

fileInputEl.addEventListener('change', readMachineCode, false);
