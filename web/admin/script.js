function table_search() {
    var input, filter, table, tr, td, i, txtValue;
    input = document.getElementById('tableSearchBar');
    filter = input.value.toUpperCase();
    table = document.getElementById('stockTable');
    tr = table.getElementsByTagName("tr");

    //Loop
    for (i = 0; i < tr.length; i++) {
        td = tr[i].getElementsByTagName("td")[9];
        if (td) {
            txtValue = td.textContent || td.innerText;
            if (txtValue.toUpperCase().indexOf(filter) > -1) {
                tr[i].style.display = "";
            } else {
                tr[i].style.display = 'none';
            }
        }
    }
}   

function printDiv(divID) {
    //Get the HTML of div
    var divElements = document.getElementsByClassName(divID)[0].outerHTML;
    //Get the HTML of whole page
    var oldPage = document.body.innerHTML;
    //Reset the page's HTML with div's HTML only
    document.body.innerHTML = 
      "<html><head><title></title></head><body>" + 
      divElements + "</body>";
    //Print Page
    window.print();
    //Restore orignal HTML
    //document.body.innerHTML = oldPage;

}