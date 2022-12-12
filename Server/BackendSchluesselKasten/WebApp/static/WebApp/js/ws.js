let body;
let mode;
const options = { year: 'numeric', month: 'long', day: 'numeric', hour: 'numeric', minute: 'numeric' };

export function setupWS() {
    const socket = new WebSocket(setURI());
    body = document.querySelector("tbody") || null;
    mode = document.querySelector('a.active').innerHTML;
    socket.onmessage = ({ data }) => {
        const obj = JSON.parse(data)
        body = document.querySelector("tbody") || null;
        if (obj.type == "DB_Tour_U") {
            if (mode == "Aktuell") {
                Aktuell(socket, obj);
            }
            else if (mode == "Verlauf") {
                Verlauf(socket, obj);
            }
        }
        else if (obj.type == "DB_Refresh") {
            // if (body) {
            //     body.innerHTML = "";
            //     deleteTable();
            // }
            document.querySelector(".dialog").classList.replace("open", "closed");
        }
    }
    return socket;
}
//Called funcs
let Aktuell = function (socket, obj) {
    if (body !== null) {
        testForID(socket, obj);
    }
    else {
        createTable(socket, obj);
    }
}

let Verlauf = function (socket, obj) {
    let input = document.getElementById('id_name').value

    if (input == "" || input.split(" ").reduce((prev, curr) => prev + Number(obj.name.toString().includes(curr.toString())), 0) > 0) {
        if (body !== null) {
            testForID(socket, obj)
        }
        else {
            createTable(socket, obj);
        }
    }
}

//Helpers
let testForID = (socket, obj) => {
    let test = 0;
    let temp = Array.from(body.children).filter(item => item.id == obj.id.toString())
    if (temp.length == 0) {
        createRow(socket, obj);
    }
    if (temp.length > 0) {
        if (obj.back) {
            if (mode === "Verlauf") {
                update(temp[ 0 ], obj)
            }
            else if (mode === "Aktuell") {
                body.removeChild(temp[ 0 ]);
                deleteTable();
            }
        }
    }
}

let createTable = (socket, obj) => {
    if (mode === "Aktuell") {
        document.getElementById("table").innerHTML = '<table class="table table-striped table-bordered"><thead class="table-dark"><tr><th class="fw-light">Name</th><th class="fw-light">Haus</th><th class="fw-light">Zielort</th><th class="fw-light">Start</th><th class="fw-light">Vermutlich zurück</th></tr></thead><tbody class="infinite-container"></tbody></table>';
    }
    else {
        document.getElementById("table").innerHTML = '<table class="table table-striped table-bordered"><thead class="table-dark"><tr><th class="fw-light">Name</th><th class="fw-light">Haus</th><th class="fw-light">Zielort</th><th class="fw-light">Start</th><th class="fw-light">Ankunft</th></tr></thead><tbody class="infinite-container"></tbody></table>';
    }
    var infinite = new Waypoint.Infinite({
        element: document.querySelector('.infinite-container')
    });
    createRow(socket, obj);
}

let deleteTable = () => {
    if (body.childElementCount === 0) {
        document.getElementById("table").innerHTML = "<div id='Placeholder' class='h-100 w-100 text-center'>Keine Einträge!</div>";
    }
}

let createRow = (socket, obj) => {
    body = document.querySelector("tbody");
    var row = body.insertRow(0);
    row.title = "Noch unterwegs"
    row.id = obj.id;
    row.classList.add("infinite-item")
    if (mode === "Verlauf") { row.classList.add("away") }
    let { name: Name, house, target, start, end } = obj;
    let values = [ Name, house, target, new Date(start).toLocaleDateString(obj.lang_code, options), (mode === "Aktuell") ? new Date(end).toLocaleDateString(obj.lang_code, options) : "" ]
    let cell;
    for (let i = 0; i < values.length; i++) {
        cell = row.insertCell(i);
        cell.innerHTML = values[ i ]
    }
    row.onclick = function () { comeBack(socket, row) }
}

let update = (item, obj) => {
    let endCell = Array.from(item.children);
    endCell = endCell[ endCell.length - 1 ];
    endCell.innerHTML = new Date(obj.end).toLocaleDateString(obj.lang_code, options);
    item.title = "Zurück";
    item.classList.remove("away");
    item.classList.add("back")
}

let setURI = () => {
    let loc = window.location, new_uri;
    new_uri = loc.protocol === "https:" ? "wss:" : "ws:";
    new_uri += "//" + loc.host + "/ws/";
    return new_uri
}

export function refreshDB(socket) {
    let bool = window.confirm("Wollen Sie wirklich die Datenbank überschreiben?")
    if (bool) {
        console.log("Refreshing");
        document.querySelector(".dialog").classList.replace("closed", "open");
        const msg = {
            type: "refresh"
        }
        socket.send(
            JSON.stringify(msg)
        )
    }
    console.log("Canceled")
}

export function printPDF(socket) {
    const msg = {
        type: "print"
    }
    socket.send(
        JSON.stringify(msg)
    )
}

export function comeBack(socket, html) {
    const msg = {
        type: "update",
        id: html.id
    }
    socket.send(
        JSON.stringify(msg)
    )
}
