

class Cookie {

    static getValueCookie(value){
        let cookies = document.cookie.split(';')
        let cookieValue = "";
        
        cookies.forEach(cookie => {
            if (cookie.search(value) != -1){
                cookieValue = cookie.slice(value.length + 1, cookie.length)
            }
        });

        return cookieValue
    }
    
}