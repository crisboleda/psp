
class Tag {

    static get(type, name){
        if (type == 'id') return document.getElementById(name)
        else if (type == 'name') return document.getElementsByName(name)
        else if (type == 'class') return document.getElementsByClassName(name)
    }
}