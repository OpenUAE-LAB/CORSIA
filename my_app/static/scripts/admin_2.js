document.addEventListener("DOMContentLoaded", function () {
    const selectAllCheckbox = document.getElementById("select-all");

    selectAllCheckbox.addEventListener("change", (event) => {
        var checkboxes = document.querySelectorAll('#table-body .ckb');
        console.log(checkboxes);
        checkboxes.forEach((checkbox) => {
            checkbox.checked = event.target.checked;
            console.log('EnteredSelectAll_check');
        });
    });

    const tbody = document.getElementById("table-body");

    const filterIcon = document.querySelector('#search');
    const dateInput = document.getElementById("month_input");
    const y = new Date().getFullYear();

    dateInput.min = new Date(y - 2, 0, 1).toISOString().split("T")[0];
    dateInput.max = new Date(y + 1, 0, 1).toISOString().split("T")[0];

    console.log(filterIcon);
    console.log(dateInput);

    filterIcon.addEventListener('click', function () {
        console.log("clicked");
        console.log(dateInput.style.display);
        if (dateInput.style.display === "none") {
            dateInput.style.display = "block";
            // dateInput.focus();
        } else {
            dateInput.style.display = "none";
        }
    });

    dateInput.addEventListener("change", (event) => {
        const selectedDate = new Date(event.target.value);
        const selectedMonth = selectedDate.getMonth();
        const selectedYear = selectedDate.getFullYear();
        const dateRegex = /(\d{2}\/\d{2}\/\d{4})/; // matches date in mm/dd/yyyy format
        [...tbody.children].forEach(tr => {
            tr.querySelectorAll("td").forEach((td) => {
                const tdDateMatch = td.textContent.trim().match(dateRegex);
                if (tdDateMatch) {
                    const tdDate = new Date(tdDateMatch[0]);
                    console.log(tdDate.getMonth(), selectedMonth, tdDate.getFullYear(), selectedYear);
                    if (tdDate.getMonth() === selectedMonth && tdDate.getFullYear() === selectedYear) {
                        tr.style.display = "";
                    } else {
                        tr.style.display = "none";
                    }
                }
            });
        });
    });
});