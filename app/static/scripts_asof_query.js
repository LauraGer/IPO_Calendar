/**
 * Executes a query asynchronously using XMLHttpRequest.
 *
 * @param {string} value - The value to be used in the query.
 * @param {string} searchType - The type of search to be performed.
 * @param {string} elementId - The ID of the HTML element where the query result will be displayed.
 * @param {function} callback - A callback function to be called when the query completes.
 *                              The response text from the query will be passed to this function.
 */
function executeQuery(value, searchType, elementId, callback) {
    console.log("executeQuery value:", value);
    console.log("executeQuery searchType:", searchType);
    console.log("executeQuery elementId:", elementId);

    var xhr = new XMLHttpRequest();
    xhr.open("GET", "/asof/query?value=" + value + "&searchType=" + searchType, true);
    xhr.onreadystatechange = function() {
        if (xhr.readyState == 4 && xhr.status == 200) {
            console.log("executeQuery responseText:", xhr.responseText);

            // Assuming elementId is the ID of cell4
            document.getElementById(elementId).innerHTML = xhr.responseText;

            // Call the callback function with the response text
            callback(xhr.responseText);
        }
    };
    xhr.send();
}

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