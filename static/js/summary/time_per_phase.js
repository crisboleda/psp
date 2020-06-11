
// Context Chart Time
const ctxChartTimePerPhase = document.getElementById('chartTimePerPhase').getContext('2d')
const ctxChartTotalTimePerPhase = document.getElementById('chartTotalTime').getContext('2d')
const ctxChartTimePercentage = document.getElementById('chartTimePercentage').getContext('2d')

// Title Counter Actual Time
const spanActualTime = document.getElementById('spanActualTime')
const spanTotalTime = document.getElementById('spanTotalTime')

// Loader Tab Time per phase
const summaryLoaderTimePerPhase = document.getElementById('summaryLoaderTimePerPhase')

apiService.request(`/programs/${idProgram}/data_time_per_phase/`, {}, 'GET').then(response => {
    response.json().then(data => {

        summaryLoaderTimePerPhase.classList.add('d-none')
        summaryLoaderTimePerPhase.nextElementSibling.classList.remove('d-none')

        let labelsActualTime = []
        let minutesPerPhase = []

        let labelsTotalTime = []
        let minutesTotalTime = []

        let dataPercentage = []

        let totalTime = 0

        console.log(data)

        data.time_per_phase.map(phase => {
            labelsActualTime.push(phase.name)
            minutesPerPhase.push(phase.total_time)

            spanActualTime.textContent = parseInt(spanActualTime.textContent) + phase.total_time
        })

        data.time_per_phase_to_date.map(phase => {
            labelsTotalTime.push(phase.name)
            minutesTotalTime.push(phase.total_time)

            spanTotalTime.textContent = parseInt(spanTotalTime.textContent) + phase.total_time
            totalTime += phase.total_time
        })

        minutesTotalTime.map(value => {
            dataPercentage.push(calculatePercentageTime(value, totalTime))
        })
        
        CreatorChart.createChartBar(ctxChartTimePerPhase, labelsActualTime, minutesPerPhase, "Time per phase ACTUAL-PROGRAM (Minutes)")
        CreatorChart.createChartBar(ctxChartTotalTimePerPhase, labelsTotalTime, minutesTotalTime, "Time total per phase TO-DATE (Minutes)")
        CreatorChart.createChartDoughnut(ctxChartTimePercentage, labelsTotalTime, dataPercentage, "Time per phase TO-DATE (Percentage)")
    })
})

function calculatePercentageTime(value, total) {
    return ((100 / total) * value ).toFixed(2)
}


