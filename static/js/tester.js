let my_ip = "0.0.0.0";
fetch("https://api.ipify.org/").then(response => response.text()).then(data => my_ip = data);

let hash = "";
let attempt = 0;
let domain = "http://webtracker.duckdns.org:8888/";

function send_track() {
    fetch(`${domain}test`,
        {
            method: "POST",
            mode: "no-cors",
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
}

send_track();
