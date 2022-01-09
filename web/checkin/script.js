function CheckInForm() {
    let part_number = document.getElementById("CheckInPartNumber").value;
    let qty = document.getElementById("CheckInQty").value;
    let notes = document.getElementById("CheckInNotes").value;
    var xhttp = new XMLHttpRequest();
    xhttp.open("POST", "/pst/checkin_submit");
    xhttp.setRequestHeader("Content-Type", "application/json");
    xhttp.onload = function() {
        //document.getElementById("checkoutHistory").innerHTML = this.responseText
        alert(this.responseText)
        document.getElementById("checkInID").reset();
    };
    var data = JSON.stringify({"part_number":part_number, "qty":qty, "notes":notes});
    xhttp.send(data);
}