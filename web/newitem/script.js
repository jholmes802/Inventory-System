function newItem() {
    let inputs = document.getElementById("newItemForm").getElementsByTagName("input");
    let sending = {}
    for (var i = 0; i < inputs.length; i++) {
        let id = inputs[i].id;
        let val = inputs[i].value;
        sending[id] = val
    }
    console.log(sending)
    let data = JSON.stringify(sending);
    var xhttp = new XMLHttpRequest();
    xhttp.open("POST", "/pst/newitem");
    xhttp.setRequestHeader("Content-type", "application/json");
    xhttp.onload = function() {
        alert(this.responseText);
        document.getElementById("newItemForm").reset();
    }
    xhttp.send(data);
} 

