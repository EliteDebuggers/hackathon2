async function computeHMAC(secret, message) {
    const encoder = new TextEncoder();
    const key = await crypto.subtle.importKey(
        'raw', 
        encoder.encode(secret),
        { name: 'HMAC', hash: 'SHA-256' },
        false, 
        ['sign']
    );
    const signatureBuffer = await crypto.subtle.sign('HMAC', key, encoder.encode(message));
    return Array.from(new Uint8Array(signatureBuffer))
        .map(b => b.toString(16).padStart(2, '0')).join('');
}

async function sendSignedRequest() {
    const usernameInput = document.getElementById("username");
    const outputField = document.getElementById("output");
    const button = document.querySelector("button");

    const username = usernameInput.value;
    const timestamp = Math.floor(Date.now() / 1000).toString();
    const body = JSON.stringify({ username });

    // PRAMAN signature payload 
    const message = `${timestamp}:POST:/api/v1/delete-user:${body}`;
    
    if (button) {
        button.disabled = true;
        button.innerText = "Sending...";
    }

    try {
        const signature = await computeHMAC(SHARED_SECRET, message);
        const res = await fetch(ENDPOINT, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-Timestamp": timestamp,
                "X-Signature": signature
            },
            body: body
        });

        const data = await res.json();
        outputField.textContent = JSON.stringify(data, null, 2);
    } catch (err) {
        outputField.textContent = "Error: " + err.message;
    } finally {
        if (button) {
            button.disabled = false;
            button.innerText = "Delete User";
        }
    }
}