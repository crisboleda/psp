

class UtilUrl {

    getParameterByName(name) { 
        return decodeURIComponent((new RegExp('[?|&]' + name + '=' + '([^&;]+?)(&|#|;|$)').exec(location.search)||[,""])[1].replace(/\+/g, '%20'))||null; 
    } 

    changeUrlParam (param, value) { 
        var currentURL = window.location.href+'&'; 
        var change = new RegExp('('+param+')=(.*)&', 'g'); 
        var newURL = currentURL.replace(change, '$1='+value+'&'); 
 
        if (this.getParameterByName(param) !== null){
            try { 
                window.history.replaceState('', '', newURL.slice(0, - 1) ); 
                console.log(window.history)
            } catch (e) { 
                console.log(e); 
            } 

        } else { 
            var currURL = window.location.href; 

            if (currURL.indexOf("?") !== -1){ 
                window.history.replaceState('', '', currentURL.slice(0, - 1) + '&' + param + '=' + value); 
            } else { 
                window.history.replaceState('', '', currentURL.slice(0, - 1) + '?' + param + '=' + value); 
            } 
        } 
    }

}
