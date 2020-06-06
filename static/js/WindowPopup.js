

class WindowPopup {

    static showWindow(url){
        let width = "1000"
        let height = "700"
        let scrollbars = "SI"

        window.open(url, "ventana1", `width=${width}, height=${height}, scrollbars=${scrollbars}`)
    }

}