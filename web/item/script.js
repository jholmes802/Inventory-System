function printBarcode() {
    const queryString = window.location.search;
    const urlParams = new URLSearchParams(queryString);
    let part_number = urlParams.get("partUUID");
    var xhttp = new XMLHttpRequest();
    xhttp.open("POST", "/pst/printBarcode");
    xhttp.setRequestHeader("Content-Type", "application/json");
    xhttp.onload = function() {
        //document.getElementById("checkoutHistory").innerHTML = this.responseText
        alert(this.responseText);
    };
    var data = JSON.stringify({"part_uuid":part_number});
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
function itemstatus (stat) {
    const queryString = window.location.search;
    const urlParams = new URLSearchParams(queryString);
    let part_number = urlParams.get("partUUID");
    let xhttp = new XMLHttpRequest
    let data = JSON.stringify({"part_uuid":part_number, "status":stat})
    xhttp.open("POST", "/pst/itemstatus");
    xhttp.setRequestHeader("Content-Type", "application/json");
    xhttp.onload = function() {
        alert(this.responseText);
        window.location.replace("/");
    };
    xhttp.send(data);
}
function checkio() {
    document.getElementsByClassName("checkIO")[0].style.display = "block"
}
function checkin() {
    const queryString = window.location.search;
    const urlParams = new URLSearchParams(queryString);
    let part_uuid = urlParams.get("partUUID");
    let qty = document.getElementById("qty").value;
    var xhttp = new XMLHttpRequest();
    xhttp.open("POST", "/pst/checkin_submit");
    xhttp.setRequestHeader("Content-Type", "application/json");
    xhttp.onload = function() {
        //document.getElementById("checkoutHistory").innerHTML = this.responseText
        alert(this.responseText)
        document.getElementById("qty").value = "";
        document.getElementsByClassName("checkIO")[0].style.display = ""
    };
    var data = JSON.stringify({"part_uuid":part_uuid, "qty":qty});
    xhttp.send(data);
}
function checkout() {
    const queryString = window.location.search;
    const urlParams = new URLSearchParams(queryString);
    let part_uuid = urlParams.get("partUUID");
    let qty = document.getElementById("qty").value;
    var xhttp = new XMLHttpRequest();
    xhttp.open("POST", "/pst/checkout_submit");
    xhttp.setRequestHeader("Content-Type", "application/json");
    xhttp.onload = function() {
        //document.getElementById("checkoutHistory").innerHTML = this.responseText
        alert(this.responseText)
        document.getElementById("qty").value = "";
        document.getElementsByClassName("checkIO")[0].style.display = ""
    };
    var data = JSON.stringify({"part_uuid":part_uuid, "qty":qty});
    xhttp.send(data);
}