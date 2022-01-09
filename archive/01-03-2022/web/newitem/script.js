function checkout() {
    let part_name = document.getElementById("part_number").value;
    let qty = document.getElementById("qty").value;
    var xhttp = new XMLHttpRequest();
    xhttp.onload = function() {
        document.getElementById("checkoutHistory").innerHTML = this.responseText
    }
    xhttp.open("POST", "checkout?prt_num=" + part_name + "&qty=" + qty);
    xhttp.send();
}

