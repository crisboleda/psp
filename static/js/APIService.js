

class APIService {

    init = {
        method: null,
        credentials: 'include',
        headers: {
            "X-CSRFToken": Cookie.getValueCookie('csrftoken'),
            "Accept": "application/json",
            "Content-Type": "application/json"
        },
        body: {}
    }

    async request(url, body = {}, method){
        this.init.method = method
        this.init.body = JSON.stringify(body)

        const response = await fetch(url, this.init)
        return response
    }

}