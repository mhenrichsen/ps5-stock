let table = document.querySelector("table");

const head = ["Butik", "Model", "Lagerstatus", "Sidst opdateret"];

window.addEventListener("load", function () {
    const data = '';
    fetch('/status')
        .then(response => response.json())
        .then(function(data) {
            let thead = table.createTHead();
            let row = thead.insertRow();

            for (key of head) {
                let th = document.createElement("th");
                let text = document.createTextNode(key);
                th.appendChild(text);
                row.appendChild(th);
            }

            for (const i of Object.entries(data)) {
                const product_url = i[1]["product_url"];
                const product_name = i[1]["product_name"];
                const store = i[1]["store"];
                const time = i[1]["time"];
                const stock = i[1]["stock"];
                let therow = [store, product_name, stock, time];
                let row = table.insertRow();
                if (i[1]["stock"] == "På lager") {
                    row.className = 'table-success'
                } else {
                    row.className = 'table-danger'
                }
                for (ce of therow) {
                    if (ce.includes('lager')) {
                        let cell = row.insertCell();
                        let link = document.createElement("a");
                        var href = product_url;
                        link.href = href;
                        link.innerHTML = ce;
                        cell.appendChild(link);
                    } else {
                        let cell = row.insertCell();
                        let text = document.createTextNode(ce);
                        cell.appendChild(text);
                    }
                }
            }



        });

});
document.forms['form-email'].addEventListener('submit', (event) => {
    event.preventDefault();
    const email = document.getElementById('email-adress').value;

    fetch('/add-email?email=' + email)
        .then(response => response.json())
        .then(() => {
            document.getElementById('email-adress').value = '';
            document.getElementById('emailHelp').innerHTML = "Vi har tilføjet din email adresse";
        });
});