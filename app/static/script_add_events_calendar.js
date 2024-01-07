// Function to fetch data from the API endpoint
function fetchData() {
    fetch('/calendar/data')  // Replace this URL with your FastAPI endpoint
        .then(response => response.json())
        .then(data => {
            // Use the fetched data in your JavaScript code
            console.log(data);

            // Assuming data is an array of entries, each having a 'date' property
            // Loop through the fetched data and populate the calendar based on dates
            data.forEach(entry => {
                const entryDate = new Date(entry.date); // Convert date string to Date object

                // Find the corresponding date in the calendar and mark it with the entry details
                // This is a hypothetical function, you need to define your logic here
                markDateInCalendar(entryDate, entry.details);
            });
        })
        .catch(error => console.error('Error:', error));
}
function markDateInCalendar(date, details) {
    const calendarCells = document.getElementsByClassName('calendar-container')[0];
    const cell = findCellForDate(date);
    cell.style.backgroundColor = 'red'; // Change color to red for visibility
    cell.addEventListener('click', () => showEntryDetails(details));

}
// This function is a placeholder to find a cell corresponding to the date
function findCellForDate(date) {
            // Hypothetical logic to find the cell for the given date
            // You'd need to implement this according to your calendar representation
            // For example, you might convert the date to a row/column index
            // and then find the corresponding HTML element in your calendar grid
            // Replace this with your logic to identify the correct cell for the date
            return document.getElementById('cell-id-for-date-' + date.getDate());
        }
// Call the function to fetch data and populate the calendar
fetchData();