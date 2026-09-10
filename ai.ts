//% color="#7450e8" icon="\uf544" block="AI"
namespace AI {
    /**
     * Zwraca tekst bez transportu. Kandydat Identity sprawdza import i wykonanie
     * zwykłego Extension w rzeczywistym świecie Minecraft.
     */
    //% blockId=ai_ask block="AI zapytaj $text"
    //% text.defl="hello"
    export function ask(text: string): string {
        return text
    }
}
