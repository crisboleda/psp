

class WindowPopup {

    static showWindow(url){
        let width = "900"
        let height = "500"
        let scrollbars = "SI"

        window.open(url, "ventana1", `width=${width}, height=${height}, scrollbars=${scrollbars}`)
    }

}