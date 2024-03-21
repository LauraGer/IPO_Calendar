


$(document).ready(function () {
    // intitial setup
    var selectedValue = $('#listnameSelect').val();
    handleSelectChange(selectedValue, $('#newValueContainer'));

    // Event listener for the first element
    $('#listnameSelect').on('change', function () {
        $('#newValueContainer').hide();
        $('#queryResult').show();
        var selectedValue = $(this).val();
        handleSelectChange(selectedValue, $('#newValueContainer'));
        if (selectedValue !== 'createNew') {
            var searchType = 'listName';
            return_value = executeQuery(selectedValue, searchType, 'queryResult');
            console.log("listnameSelect return_value:", return_value);
        }
    });

    // Event listener for the second element
    $('#symbols').on('change', function () {
        $('#searchSymbolContainer').hide();
        var selectedValue = $(this).val();
        handleSelectChange(selectedValue, $('#searchSymbolContainer'));
        handleAsOfDate(selectedValue);
    });

    $('#asOfDate').on('change', function () {
        var selectedDate = $(this).val();
        var searchType = 'asOfDateChange';
        var selectedValue = $('#symbols').val();
        return_value = executeQuery(selectedDate, searchType, 'priceResult' )
        console.log("asOfDate return_value:", return_value);
        handleAsOfDate(selectedValue, selectedDate);
    });

    $('#toggleButton').on('change', function () {
        const searchStockContainer = document.getElementById('searchStockContainer');
        searchStockContainer.style.display = this.checked ? 'block' : 'none';
    });

    $('#open-popup-btn').click(function (e) {
        e.preventDefault(); // Prevent the default form submission behavior
        var stockNewValue = $('#stockNew').val();
        var stockSourceValue = $('#stockSource:checked').val(); // Get the value of the checked radio button

        // Log or alert the value of stockSourceValue for debugging
        console.log("Selected stock source:", stockSourceValue);

        // Open the popup window with the stockNew value as a query parameter
        var popupUrl = '/asof/popup?stockNew=' + encodeURIComponent(stockNewValue) + '&stockSource=' + encodeURIComponent(stockSourceValue);
        var popupWindow = window.open(popupUrl, 'Popup', 'width=600,height=400');
    });

});

window.onload = function() {
    // addRow();
};

function handleSelectChange(selectedValue, $targetElement) {
    if (selectedValue) {
        if (selectedValue === 'createNew') {
            $('#queryResult').hide();
            $targetElement.show();
        }
    }
}

// ADD STOCK TABLE
function addRow() {
    var table = document.getElementById("asOfTable").getElementsByTagName("tbody")[0];
    var newRow = table.insertRow();

    // Insert cells and populate with select and input fields
    var cell1 = newRow.insertCell(0);
    var cell2 = newRow.insertCell(1);
    var cell3 = newRow.insertCell(2);
    var cell4 = newRow.insertCell(3);
    var cell5 = newRow.insertCell(4);

    // Populate cell 1 with select dropdown
    var selectHtml = '<select id="symbols" name="symbols" required class="required">>';
    selectHtml += '<option value="" selected disabled>Select or search ...</option>';
    // selectHtml += '<option value="createNew">Search Symbol</option>';
    for (var i = 0; i < symbols_dropdown.length; i++) {
        selectHtml += '<option value="' + symbols_dropdown[i] + '">' + symbols_dropdown[i] + '</option>'
    }
    selectHtml += '</select>';
    cell1.innerHTML = selectHtml;

    cell2.innerHTML = '<input type="date" id="asOfDate" name="asOfDate" class="asofdate-input" required>';
    cell3.innerHTML = '<input type="number" name="volume" class="volume-input" placeholder="enter volumne..." required>';
    cell4.innerHTML = '<input type="number" id="price"  name="price" step="0.01"  min="0"  class="price-input" required>';
    // cell5.innerHTML = '<span class="remove-icon" onclick="removeRow(this.parentNode.parentNode)">&#128465;</span>';
}

// AS OF DATE FOR TABLE
function handleAsOfDate(selectedValue, asOfDateValue){
    if (asOfDateValue === undefined) {
        console.log("selectedValue:", selectedValue);
        // symbols_with_data - variable from html template file
        var minDateKeyEntry = symbols_with_data.find(entry => {
            // console.log('Entry:', entry.symbol);
            return entry.symbol === selectedValue;
        });
        var set_AsOfDate = $('#asOfDate').val();
        if (minDateKeyEntry.min_datekey !== set_AsOfDate ){
            // HERE IT SHOULD UPDATE AS SOON AS OF DATE CHANGES FOR FUTURE
        }
        if (minDateKeyEntry){
            $('#asOfDate').val(minDateKeyEntry.min_datekey);
            $('#price').val(minDateKeyEntry.avg_price_o_h_l_c.toFixed(2));
        }
        console.log("minDateKeyEntry:", minDateKeyEntry);
    } else {
        console.log(selectedValue, asOfDateValue)
    }
}

// Function to remove a row from the table
function removeRow(row) {
    row.parentNode.removeChild(row);
}

