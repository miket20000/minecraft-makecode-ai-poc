//% color="#7450e8" icon="\uf544" block="AI"
namespace AI {
    /** Kandydat Direct HTTP: sprawdza oba znane mechanizmy bez obejść. */
    //% blockId=ai_ask block="AI zapytaj $text"
    //% text.defl="hello"
    export function ask(text: string): string {
        fetch("http://127.0.0.1:8765/echo", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ text: text })
        })
        pxt.Util.requestAsync({
            url: "http://127.0.0.1:8765/echo",
            method: "POST",
            data: { text: text }
        })
        return "AI_ERROR:direct-http-no-sync-result"
    }
}
