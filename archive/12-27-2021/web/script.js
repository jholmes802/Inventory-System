function checkout() {
    let x = document.getElementById("checkout_form");
    var text = "";
    var i = 0;
    for (i=0; i < x.length -1; i++) {
        text += x.elements[i].value + "<br>";
    }
    XMLHttpRequest.send(text)
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