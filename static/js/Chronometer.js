

class Chronometer {

    inputHours = null
    inputMinutes = null
    inputSeconds = null
    totalSeconds = 0
    counter = null
    idTimeLog = null
    serviceChronometer = null

    constructor(inputHours, inputMinutes, inputSeconds, totalSeconds, idTimeLog){
        // Chronometer input's
        this.inputHours = inputHours
        this.inputMinutes = inputMinutes
        this.inputSeconds = inputSeconds
        this.total_seconds = totalSeconds

        // ID time log
        this.idTimeLog = idTimeLog

        // This service allow us to update the time in server
        this.serviceChronometer = new ServiceChronometer()
    }

    updateValues(){
        var [hours, minutes, seconds] = ParseTime.getFormatTime(this.totalSeconds)
        
        this.inputHours.textContent = hours
        this.inputMinutes.textContent = minutes
        this.inputSeconds.textContent = seconds
    }

    refreshTimer(){
        this.totalSeconds += 1
        this.updateValues()
    }

    start(){
        this.counter = setInterval(this.refreshTimer.bind(this), 1000)
    }

    async pause(){
        if (this.counter) clearInterval(this.counter)
        const result = await this.serviceChronometer.updateTime(this.totalSeconds, this.idTimeLog, 1)

        console.log(result)
    }

}

