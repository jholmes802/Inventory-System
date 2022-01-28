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
function editPartForm() {
    let parttable = document.getElementsByClassName("partSpecs")[0];
    parttable = parttable.getElementsByTagName("tr");
    i = 0
    for (let i = 0; i < parttable.length; i ++) {
        parttable[i].getElementsByTagName("td")[0].innerHTML = "<input type='text' value='" + parttable[i].getElementsByTagName("td")[0].innerHTML + "'></input>";
    }
    document.getElementById("editButton").innerHTML = "Save Item";
    document.getElementById("editButton").onclick = function() {savePartForm();}
}
function savePartForm() {
    let parttable = document.getElementsByClassName("partSpecs")[0];
    parttable = parttable.getElementsByTagName("tr");
    let sending = {}
    for (let i = 0; i < parttable.length; i ++) {
        let val = parttable[i].getElementsByTagName("input")[0].value;
        let id = String(parttable[i].getElementsByTagName("th")[0].innerHTML).toLowerCase().replace(/ /g, "_");
        parttable[i].getElementsByTagName("td")[0].innerHTML = val;
        sending[id] = val;
    }
    sending = JSON.stringify(sending);
    console.log(sending)
    xh = new XMLHttpRequest();
    xh.open("POST", "/pst/editpart");
    xh.setRequestHeader("Content-type", "application/json");
    xh.onload = function() {
        alert(this.responseText);
        document.getElementById("editButton").innerHTML = "Edit Item";
        document.getElementById("editButton").onclick = function() {editPartForm();}
    }
    xh.send(sending)
}