function editField(field) {
  const display = document.getElementById(`${field}-display`);
  const input = document.getElementById(`${field}-input`);
  if (display && input) {
    display.classList.add('hidden');
    input.classList.remove('hidden');
    input.focus();
  }
}

function eraseField(field) {
  const display = document.getElementById(`${field}-display`);
  const input = document.getElementById(`${field}-input`);
  if (input) {
    input.value = '';
    input.classList.remove('hidden');
  }
  if (display) {
    display.innerText = '[Erased]';
  }
}
