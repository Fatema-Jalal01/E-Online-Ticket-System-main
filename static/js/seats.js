// Get the selected seat numbers from local storage.
var selectedSeatNumbers = JSON.parse(localStorage.getItem('selectedSeats'));

// If there are selected seats in local storage, mark them as selected.
if (selectedSeatNumbers) {
  seats.forEach(seat => {
    if (selectedSeatNumbers.includes(seat.dataset.seat)) {
      seat.classList.add('selected');
      seat.checked = true; // Set the checkbox as checked as well
      if (bookedSeats.includes(seat.dataset.seat)) {
        seat.disabled = true; // Disable the checkbox for booked seats
      }
    }
  });
}
