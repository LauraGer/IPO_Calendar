// Retrieve cell data with associated entries from Python (rendered into HTML)
const cellData = [
  { date: "2023-12-25", entry: "CHECK THIS OUT" },
  { date: "2023-01-05", entry: "Example entry for 2023-01-05" },
  // Add more entries with their dates and details
  // ...
];

// Function to create the calendar grid
function createCalendar() {
  const calendar = document.getElementById("calendar");

  // Loop to create 6 rows and 7 columns for the calendar
  for (let i = 0; i < 6; i++) {
      for (let j = 0; j < 7; j++) {
          const cell = document.createElement("div");
          cell.className = "calendar-cell";
          const currentDate = cellData[i * 7 + j]?.date; // Get date from cellData
          if (currentDate) {
              cell.textContent = new Date(currentDate).getDate();
              cell.setAttribute("data-entry", cellData[i * 7 + j].entry); // Attach entry details as data attribute
          }
          calendar.appendChild(cell);

          // Add event listener for hover over each cell
          cell.addEventListener("mouseover", function(event) {
              const entryDetails = event.target.getAttribute("data-entry");
              if (entryDetails) {
                  const entryDetailsDiv = document.getElementById("entry-details");
                  entryDetailsDiv.textContent = entryDetails;
                  entryDetailsDiv.style.display = "block";
                  entryDetailsDiv.style.left = (event.pageX + 10) + "px"; // Adjust position
                  entryDetailsDiv.style.top = (event.pageY + 10) + "px"; // Adjust position
              }
          });

          // Hide entry details on mouseout
          cell.addEventListener("mouseout", function() {
              document.getElementById("entry-details").style.display = "none";
          });
      }
  }
}

// Call the function to generate the calendar grid
createCalendar();

/*
 * This code is licensed under the MIT License.
 *
 * Copyright 2024 Laura Gerlach
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in all
 * copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 * SOFTWARE.
 */