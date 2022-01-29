function CheckoutForm() {
    let part_number = document.getElementById("CheckOutPartNumber").value;
    let qty = document.getElementById("CheckOutQty").value;
    let notes = document.getElementById("CheckOutNotes").value;
    var xhttp = new XMLHttpRequest();
    xhttp.open("POST", "/pst/checkout_submit");
    xhttp.setRequestHeader("Content-Type", "application/json");
    xhttp.onload = function() {
        //document.getElementById("checkoutHistory").innerHTML = this.responseText
        alert(this.responseText)
        document.getElementById("checkOutForm").reset();
    };
    var data = JSON.stringify({"part_uuid":part_number, "qty":qty, "notes":notes});
    xhttp.send(data);
}