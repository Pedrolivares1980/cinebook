document.addEventListener('DOMContentLoaded', function() {
    // Get the booking form by its ID
    const bookingForm = document.getElementById('bookingForm');
    // Get the showtime ID from the data attribute of a script tag
    const showtimeId = document.querySelector('script[data-showtime-id]').getAttribute('data-showtime-id');
     // Get the container where seat selections are displayed
    const seatSelectionContainer = document.getElementById('seatSelection');

    // Initialize the Bootstrap modal with animation disabled
    var confirmationModal = new bootstrap.Modal(document.getElementById('confirmationModal'), {
        keyboard: false, // Prevent closing the modal with the keyboard
        animation: false // Disable animation for the modal
    });

    // Event listener for the form submission
    bookingForm.addEventListener('submit', function(event) {
        event.preventDefault(); // Prevent the form from submitting immediately

        // Show the confirmation modal
        confirmationModal.show();
    });

    // When the confirm button in the modal is clicked
    document.getElementById('confirmBooking').addEventListener('click', function () {
        // Submit the form programmatically
        bookingForm.submit();
    });

    // Fetch and display seat availability
    fetchSeatAvailability(showtimeId);

    async function fetchSeatAvailability(showtimeId) {
        try {
            const response = await fetch(`/bookings/seats/${showtimeId}/`);
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            const data = await response.json();
            // Render the seats based on availability data
            renderSeats(data.seats);
        } catch (error) {
            console.error('Error fetching seat availability:', error);
        }
    }

    // Function to render seats in the UI
    function renderSeats(seats) {
        seatSelectionContainer.innerHTML = ''; // Clear previous seats

        // Create and add the screen div at the top
        const screenDiv = document.createElement('div');
        screenDiv.classList.add('cinema-screen');
        screenDiv.textContent = 'Screen';
        seatSelectionContainer.appendChild(screenDiv);

        // Group seats by row for rendering
        const seatsByRow = groupSeatsByRow(seats);

        // Render each row and its seats
        Object.keys(seatsByRow).sort().forEach(rowLetter => {
            const rowDiv = createRowDiv(rowLetter);
            seatsByRow[rowLetter].forEach(seat => {
                const seatDiv = createSeatDiv(seat);
                rowDiv.appendChild(seatDiv);
            });
            seatSelectionContainer.appendChild(rowDiv);
        });
    }

    // Function to group seats by their row letters
    function groupSeatsByRow(seats) {
        return seats.reduce((acc, seat) => {
            (acc[seat.row_letter] = acc[seat.row_letter] || []).push(seat);
            return acc;
        }, {});
    }

    // Function to create a div for a row of seats
    function createRowDiv(rowLetter) {
        const rowDiv = document.createElement('div');
        rowDiv.classList.add('seat-row');
        const rowLabel = document.createElement('div');
        rowLabel.textContent = rowLetter;
        rowLabel.classList.add('row-label');
        rowDiv.appendChild(rowLabel);
        return rowDiv;
    }

    // Function to create a div for an individual seat
    function createSeatDiv(seat) {
        const seatDiv = document.createElement('div');
        seatDiv.classList.add('seat');
    
        // Create a checkbox for selecting the seat
        const seatCheckbox = document.createElement('input');
        seatCheckbox.type = 'checkbox';
        seatCheckbox.id = `seat-${seat.id}`;
        seatCheckbox.name = 'seats';
        seatCheckbox.value = seat.id;
        // Disable if the seat is already reserved
        seatCheckbox.disabled = seat.is_reserved;
    
        const label = document.createElement('label');
        label.htmlFor = `seat-${seat.id}`;
    
        // Display seat info (row and number)
        const seatInfo = document.createElement('span');
        seatInfo.textContent = `${seat.row_letter}${seat.seat_number}`;
        seatInfo.classList.add('seat-info');
    
        // Add elements to the seat div
        seatDiv.appendChild(seatCheckbox);
        seatDiv.appendChild(label);
        seatDiv.appendChild(seatInfo);
    
        return seatDiv;
    }
    
});
