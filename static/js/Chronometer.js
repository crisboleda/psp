

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
        this.totalSeconds = totalSeconds

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

    async restart(){

        this.start()

        const url = `http://localhost:8000/timelogs/${this.idTimeLog}/restart/`
        const result = await this.serviceChronometer.put(url, {})

        console.log(result)
    }

    async pause(){
        if (this.counter) clearInterval(this.counter)

        const url = `http://localhost:8000/timelogs/${this.idTimeLog}/pause/`

        const body = {
            delta_time: this.totalSeconds,
            is_paused: true
        }

        const result = await this.serviceChronometer.put(url, body)

        console.log(result)
    }

    async stop(){
        if (this.counter) clearInterval(this.counter)

        const url = `http://localhost:8000/timelogs/${this.idTimeLog}/stop/`

        const body = {
            delta_time: this.totalSeconds,
            is_paused: true
        }

        return await this.serviceChronometer.put(url, body)
    }

}

