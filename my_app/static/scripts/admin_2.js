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
});