document.addEventListener('DOMContentLoaded', function() {
    const showtimeId = document.querySelector('script[data-showtime-id]').getAttribute('data-showtime-id');
    const seatSelectionContainer = document.getElementById('seatSelection');

    // Fetch and display seat availability
    fetchSeatAvailability(showtimeId);

    async function fetchSeatAvailability(showtimeId) {
        try {
            const response = await fetch(`/bookings/seats/${showtimeId}/`);
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            const data = await response.json();
            renderSeats(data.seats);
        } catch (error) {
            console.error('Error fetching seat availability:', error);
        }
    }

    function renderSeats(seats) {
        seatSelectionContainer.innerHTML = ''; // Clear previous seats

        const screenDiv = document.createElement('div');
        screenDiv.classList.add('cinema-screen');
        screenDiv.textContent = 'Screen';
        seatSelectionContainer.appendChild(screenDiv);

        const seatsByRow = groupSeatsByRow(seats);

        Object.keys(seatsByRow).sort().forEach(rowLetter => {
            const rowDiv = createRowDiv(rowLetter);
            seatsByRow[rowLetter].forEach(seat => {
                const seatDiv = createSeatDiv(seat);
                rowDiv.appendChild(seatDiv);
            });
            seatSelectionContainer.appendChild(rowDiv);
        });
    }

    function groupSeatsByRow(seats) {
        return seats.reduce((acc, seat) => {
            (acc[seat.row_letter] = acc[seat.row_letter] || []).push(seat);
            return acc;
        }, {});
    }

    function createRowDiv(rowLetter) {
        const rowDiv = document.createElement('div');
        rowDiv.classList.add('seat-row');
        const rowLabel = document.createElement('div');
        rowLabel.textContent = rowLetter;
        rowLabel.classList.add('row-label');
        rowDiv.appendChild(rowLabel);
        return rowDiv;
    }

    function createSeatDiv(seat) {
        const seatDiv = document.createElement('div');
        seatDiv.classList.add('seat');
    
        const seatCheckbox = document.createElement('input');
        seatCheckbox.type = 'checkbox';
        seatCheckbox.id = `seat-${seat.id}`;
        seatCheckbox.name = 'seats';
        seatCheckbox.value = seat.id;
        seatCheckbox.disabled = seat.is_reserved;
    
        const label = document.createElement('label');
        label.htmlFor = `seat-${seat.id}`;
    
        const seatInfo = document.createElement('span');
        seatInfo.textContent = `${seat.row_letter}${seat.seat_number}`;
        seatInfo.classList.add('seat-info');
    
        seatDiv.appendChild(seatCheckbox);
        seatDiv.appendChild(label);
        seatDiv.appendChild(seatInfo);
    
        return seatDiv;
    }
    
});
