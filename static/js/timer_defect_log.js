
// Controls Chronometer
const counterSeconds = document.getElementById('time_seg')
const counterMinutes = document.getElementById('time_mins')
const counterHours = document.getElementById('time_hours')

const btnPauseChronometer = document.getElementById('btn-pause-chronometer')
const btnResetChronometer = document.getElementById('btn-reset-chronometer')
const btnStopChronometer = document.getElementById('btn-stop-chronometer')

// Input number (Total time)
const inputDeltaTime = document.getElementById('time_defect_log')

// Button Create Defect
const btnCreateDefect = document.getElementById('btnCreateDefect')


// Logic chronometer
let chronometer = new ChronometerDefectLog(counterSeconds, counterMinutes, counterHours, inputDeltaTime)

btnPauseChronometer.addEventListener('click', () => {
    chronometer.pause()

    btnPauseChronometer.classList.add('d-none')
    btnResetChronometer.classList.remove('d-none')
})

btnResetChronometer.addEventListener('click', () => {
    chronometer.restart()

    btnResetChronometer.classList.add('d-none')
    btnPauseChronometer.classList.remove('d-none')
})

btnStopChronometer.addEventListener('click', () => {
    if (chronometer.totalSeconds > 0){
        chronometer.pause()

        btnCreateDefect.removeAttribute('disabled')
        btnPauseChronometer.classList.add('d-none')
        btnResetChronometer.classList.add('d-none')
        btnStopChronometer.classList.add('d-none')
    }
})