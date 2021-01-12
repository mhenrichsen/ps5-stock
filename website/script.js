let table = document.querySelector("table");

const head = ["Butik", "Model", "Lagerstatus", "Sidst opdateret"];

window.addEventListener("load", function () {
    const data = '';
    fetch('/status.json')
        .then(response => response.json())
        .then(function(data) {

            console.log(data);

            var table = $('table').DataTable({
                columns: [{ data: "store" }, 
                { data: "model" }, 
                { data: "status" },
                { data: "lastupdated" }],
                order: [[1, "desc"], [2, "desc"]],
                paging: false
            });
            for(var k of Object.entries(data))
            {
                const product = k[1];
                let row = table.row.add({
                    "store": product.store,
                    "model": product.product_name ,
                    "status": '<a href="' + product.product_url + '">' + product.stock + '</a>',
                    "lastupdated": product.time}).draw().node();

                if(product.stock !== 'Ikke på lager')
                    $(row).addClass('inStock');
                else 
                    $(row).addClass('notInStock');
            }
            
    });     
});
document.forms['form-email'].addEventListener('submit', (event) => {
    event.preventDefault();
    const email = document.getElementById('email-adress').value;

    // console.log(email);
    fetch('/add-email?email=' + email)
        .then(response => response.json())
        .then(document.getElementById('emailHelp').innerHTML = "Vi har tilføjet din email adresse");
});