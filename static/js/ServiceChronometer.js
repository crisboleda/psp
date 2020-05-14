

class ServiceChronometer {

    async put(url, body){
        let init = {
            method: 'PATCH',
            credentials: 'include',
            headers: {
                "X-CSRFToken": this.getValueCookie('csrftoken'),
                "Accept": "application/json",
                "Content-Type": "application/json"
            },
            body: JSON.stringify(body)
        }

        const response = await fetch(url, init)
        const data = await response.json()

        return data
    }

    getValueCookie(value){
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