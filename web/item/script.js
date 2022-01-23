function printBarcode() {
    const queryString = window.location.search;
    const urlParams = new URLSearchParams(queryString);
    let part_number = urlParams.get("partNumber");
    var xhttp = new XMLHttpRequest();
    xhttp.open("POST", "/pst/printBarcode");
    xhttp.setRequestHeader("Content-Type", "application/json");
    xhttp.onload = function() {
        //document.getElementById("checkoutHistory").innerHTML = this.responseText
        alert(this.responseText);
    };
    var data = JSON.stringify({"part_number":part_number});
    xhttp.send(data);
}
function editPart() {
    let parttable = document.getElementsByClassName("partSpecs")[0];
    parttable = parttable.getElementsByTagName("tr");
    i = 0
    for (let i = 0; i < parttable.length; i ++) {
        parttable[i].getElementsByTagName("td")[0].innerHTML = "test";
    }
}