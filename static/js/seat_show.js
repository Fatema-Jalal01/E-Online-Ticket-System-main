const selectedSeatsEl = document.getElementById('selected-seats');
const selectedSeats = JSON.parse(localStorage.getItem('selectedSeats'));

if (selectedSeats && selectedSeats.length > 0) {
  selectedSeatsEl.innerText = selectedSeats.join(', ');
} else {
  selectedSeatsEl.innerText = 'None';
}
