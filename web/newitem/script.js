function newItem() {
    let part_number = document.getElementById("NewPartNum").value;
    let part_name = document.getElementById("NewPartName").value;
    let part_qty = document.getElementById("NewPartQty").value;
    let part_source = document.getElementById("NewPartSource").value;
    let part_link = document.getElementById("NewPartLink").value;
    let data = JSON.stringify({"part_number":part_number, "part_name":part_name, "part_qty":part_qty, "part_source":part_source, "part_link": part_link});
    var xhttp = new XMLHttpRequest();
    xhttp.open("POST", "/pst/newitem");
    xhttp.setRequestHeader("Content-type", "application/json");
    xhttp.onload = function() {
        alert(this.responseText);
        document.getElementById("newItemForm").reset();
    }
    xhttp.send(data);
} 

