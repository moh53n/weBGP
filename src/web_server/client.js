const socket = new WebSocket("ws://localhost:8000");
var raw_updates_table = document.getElementById('raw-updates').getElementsByTagName('tbody')[0];

function append_raw_message(prefix, type, offline_for) {
    var newRow = raw_updates_table.insertRow(0);
    newRow.id = "raw-" + prefix
    var newCell0 = newRow.insertCell(0);
    var newCell1 = newRow.insertCell(1);
    var newCell2 = newRow.insertCell(2);
    if (type == "offline") {
        newCell0.innerHTML = "&#128308;";
    }
    else {
        newCell0.innerHTML = "&#128994;";
    }
    
    newCell1.innerHTML = prefix

    if (offline_for != null) {
        newCell2.innerHTML = offline_for
    }
    else {
        newCell2.innerHTML = "&#8213;";
    }
}

function parseJSON(jsonString) {
    try {
        const jsonObject = JSON.parse(jsonString);

        if (jsonObject.hasOwnProperty("offline_for")) {
            return [jsonObject.prefix, jsonObject.update, jsonObject.offline_for];
        } else {
            if (jsonObject.hasOwnProperty("prefix")) {
                return [jsonObject.prefix, jsonObject.update, null];
            }
            else {
                return null;
            }
        }
    } catch (error) {
        return "The JSON message is invalid: " + error.message;
    }
}

socket.addEventListener("open", (event) => {
    console.log("Connected to the server");
});

socket.addEventListener("message", (event) => {
    const update = parseJSON(event.data);
    append_raw_message(update[0], update[1], update[2]);
});