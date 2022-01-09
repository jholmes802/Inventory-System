function VerifyForm() {
    let part_number = document.getElementById("VerificationPartNumber").value;
    let qty = document.getElementById("VerificationPartQty").value;
    var xhttp = new XMLHttpRequest();
    xhttp.open("POST", "/pst/verify_submit");
    xhttp.setRequestHeader("Content-Type", "application/json");
    xhttp.onload = function() {
        //document.getElementById("checkoutHistory").innerHTML = this.responseText
        alert(this.responseText);
        document.getElementById("verifyFormID").reset();
    };
    var data = JSON.stringify({"part_number":part_number, "qty":qty});
    xhttp.send(data);
}

