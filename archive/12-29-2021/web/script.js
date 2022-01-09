function checkout() {
    alert("sending data..")
    let part_name = document.getElementById("part_number").value;
    let qty = document.getElementById("qty").value;
    var xhttp = new XMLHttpRequest();
    xhttp.onload = function() {
        alert(this.responseText)
    }
    xhttp.open("POST", "checkout?prt_num=" + part_name + "&qty=" + qty);
    xhttp.send();
}

function table_search() {
    var input, filter, table, tr, td, i, txtValue;
    input = document.getElementById('tableSearchBar');
    filter = input.value.toUpperCase();
    table = document.getElementById('stockTable');
    tr = table.getElementsByTagName("tr");

    //Loop
    for (i = 0; i < tr.length; i++) {
        td = tr[i].getElementsByTagName("td")[1];
        if (td) {
            txtValue = td.textContent || td.innerText;
            if (txtValue.toUpperCase().indexOf(filter) > -1) {
                tr[i].style.display = "";
            } else {
                tr[i].style.display = 'none';
            }
        }
    }
}   