let targetPage = "wss://192.168.25.44/ws/";

let ua = "Upgrade";

function rewriteUserAgentHeader(e) {
    e.requestHeaders.forEach((header) => {
        if (header.name.toLowerCase() === "connection") {
            header.value = ua;
        }
    });
    return { requestHeaders: e.requestHeaders };
}

browser.webRequest.onBeforeSendHeaders.addListener(
    rewriteUserAgentHeader,
    { urls: [ targetPage ] },
    [ "blocking", "requestHeaders" ]
);