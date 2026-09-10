namespace pxsim.AI {
    export function ask(text: string): Promise<string> {
        return fetch("http://127.0.0.1:8765/echo", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ text: text })
        }).then(response => {
            if (!response.ok) return "AI_ERROR:http_" + response.status
            return response.json().then(body => {
                if (body && typeof body.text === "string") return body.text
                return "AI_ERROR:invalid_response"
            })
        }).catch(() => "AI_ERROR:request_failed")
    }
}
