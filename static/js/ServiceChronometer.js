

class ServiceChronometer {

    async put(url, body){
        let init = {
            method: 'PATCH',
            credentials: 'include',
            headers: {
                "X-CSRFToken": Cookie.getValueCookie('csrftoken'),
                "Accept": "application/json",
                "Content-Type": "application/json"
            },
            body: JSON.stringify(body)
        }

        const response = await fetch(url, init)
        const data = await response.json()

        return data
    }
}