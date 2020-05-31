
/** 
 * @param String url
 * @param Object body
 * @param String method
**/

class APIService {

    init = {
        method: null,
        credentials: 'include',
        headers: {
            "X-CSRFToken": Cookie.getValueCookie('csrftoken'),
            "Accept": "application/json",
            "Content-Type": "application/json"
        },
        body: undefined
    }

    async request(url, body = {}, method){
        if (method.toUpperCase() != 'GET') this.init.body = JSON.stringify(body)

        this.init.method = method

        const response = await fetch(url, this.init)
        return response
    }
}