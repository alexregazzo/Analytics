let my_ip = "0.0.0.0";
fetch("https://api.ipify.org/").then(response => response.text()).then(data => my_ip = data);

let hash = "";
let attempt = 0;

function send_track() {
    fetch(`http://127.0.0.1:5000/track/?hash=${hash}`,
        {
            method: "POST",
            body: JSON.stringify(
                {
                    "hash": hash,
                    "attempt": attempt,
                    "location": window.location.href,
                    "date": new Date().toUTCString(),
                    "ip": my_ip
                }
            )
        })
        .then(function (response) {
            if (response.ok) {
                attempt++;
                return response.text()
            } else {
                if (response.status === 401) {
                    hash = "";
                    attempt++;
                    send_track();
                } else {
                    throw Error("Something is wrong!");
                }
            }
        })
        .then(function (data) {
            hash = data;
            setTimeout(`send_track()`, 10000);
        })
        .catch(function () {
            attempt++;
            setTimeout(`send_track()`, 10000);
        });
}

send_track();
window.addEventListener('beforeunload', send_track);
window.addEventListener('popstate', send_track);

