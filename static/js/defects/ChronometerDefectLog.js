

class ChronometerDefectLog {
    
    counterSeconds = null
    counterMinutes = null
    counterHours = null
    inputDeltaTime = null

    counter = null
    totalSeconds = 0

    constructor(counterSeconds, counterMinutes, counterHours, inputDeltaTime){
        this.counterSeconds = counterSeconds
        this.counterMinutes = counterMinutes
        this.counterHours = counterHours
        this.inputDeltaTime = inputDeltaTime
    }

    refrestTimer(){
        this.totalSeconds += 1
        this.inputDeltaTime.value = this.totalSeconds
        
        let [hours, minutes, seconds] = ParseTime.getFormatTime(this.totalSeconds)

        this.counterSeconds.textContent = seconds
        this.counterMinutes.textContent = minutes
        this.counterHours.textContent = hours
    }

    start(){
        this.counter = setInterval(this.refrestTimer.bind(this), 1000)
    }

    pause(){
        if (this.counter) clearInterval(this.counter)
    }

    restart(){
        this.start()
    }

    getTotalSeconds(){
        return this.totalSeconds
    }

}