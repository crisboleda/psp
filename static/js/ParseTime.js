

class ParseTime {

    static getFormatTime(data){
        let hours = Math.floor(data / 3600)
        let minutes = Math.floor((data % 3600) / 60)
        let seconds = Math.floor((data % 3600) % 60)

        hours = hours < 10 ? `0${hours}` : `${hours}`
        minutes = minutes < 10 ? `0${minutes}` : `${minutes}`
        seconds = seconds < 10 ? `0${seconds}` : `${seconds}`

        return [hours, minutes, seconds]
    }
}