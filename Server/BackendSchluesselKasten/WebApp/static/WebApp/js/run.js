import { setupWS, refreshDB, printPDF, comeBack } from './ws.js'

function run() {
    const socket = setupWS();
    document.querySelectorAll('tbody tr').forEach(item => { item.onclick = function () { comeBack(socket, item) } })
    let refreshButton = document.querySelector("#toolbar-refresh-button")
    if (refreshButton != null) {
        refreshButton.onclick = function () { refreshDB(socket) };
    }
    //document.querySelector("#toolbar-print-button").onclick = function () { printPDF(socket) };
    var infinite = new Waypoint.Infinite({
        element: document.querySelector('.infinite-container')
    });
    document.getElementById("modal-form").addEventListener("submit", subFunc)
    let p = document.querySelector("#toolbar-container");
    let c = document.querySelector("#toolbar");
    let styles = window.getComputedStyle(c);
    let height = parseInt(styles.height, 10).toString() + "px";
    p.style.height = height;
};

window.onload = run
document.onkeydown = keyPress;

function keyPress(e) {
    if (e.key == "+") {
        document.getElementById("create-modal").click();
    }
}