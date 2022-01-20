function adminBackupfunc() {
    var xhttp = new XMLHttpRequest();
    xhttp.open("POST", "/pst/backup");
    xhttp.setRequestHeader("Content-Type", "application/json");
    xhttp.onload = function() {
        //document.getElementById("checkoutHistory").innerHTML = this.responseText
        alert(this.responseText);
    };
    var data = JSON.stringify({"backup":"yes"});
    xhttp.send(data);
}