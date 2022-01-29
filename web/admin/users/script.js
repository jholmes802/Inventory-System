function newUser() {
    if (document.getElementsByClassName("newUser")[0].style.display == "") {
        document.getElementsByClassName("newUser")[0].style.display = "block";
        document.getElementsByClassName("overlay")[0].style.display = "block";
    } else {
        let inputs = document.getElementsByClassName("newUser")[0].getElementsByTagName("input");
        let sending = {}
        for (var i = 0; i < inputs.length; i++) {
            let id = inputs[i].id;
            let val = inputs[i].value;
            sending[id] = val
        }
        console.log(sending)
        let data = JSON.stringify(sending);
        var xhttp = new XMLHttpRequest();
        xhttp.open("POST", "/pst/newuser");
        xhttp.setRequestHeader("Content-type", "application/json");
        xhttp.onload = function() {
            alert(this.responseText);
            document.getElementById("newUser").reset();
            document.getElementsByClassName("newUser")[0].style.display = "none";
            document.getElementsByClassName("overlay")[0].style.display = "none";
        }
        xhttp.send(data);
    }
} 


function table_search() {
    var input, filter, table, tr, td, i, txtValue;
    input = document.getElementById('tableSearchBar');
    filter = input.value.toUpperCase();
    table = document.getElementById('stockTable');
    tr = table.getElementsByTagName("tr");

    //Loop
    for (i = 0; i < tr.length; i++) {
        td = tr[i].getElementsByTagName("td")[9];
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
