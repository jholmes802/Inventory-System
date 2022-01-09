function checkout() {
    let part_number = document.getElementById("part_number").value;
    let qty = document.getElementById("qty").value;
    var xhttp = new XMLHttpRequest();
    xhttp.open("POST", "/pst/checkout_submit");
    xhttp.setRequestHeader("Content-Type", "application/json");
    xhttp.onload = function() {
        //document.getElementById("checkoutHistory").innerHTML = this.responseText
        alert(this.responseText)
    };
    var data = JSON.stringify({"part_number":part_number, "qty":qty});
    xhttp.send(data);
}