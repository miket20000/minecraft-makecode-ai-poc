//% color="#7450e8" icon="\uf544" block="AI"
namespace AI {
    /** Kandydat Shim: implementacja znajduje się po stronie simulatora. */
    //% blockId=ai_ask block="AI zapytaj $text"
    //% text.defl="hello"
    //% promise shim=AI::ask
    export function ask(text: string): string {
        return ""
    }
}
