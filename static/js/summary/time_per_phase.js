
// Context Chart Time
const ctxChartTimePerPhase = document.getElementById('chartTimePerPhase').getContext('2d')
const ctxChartTotalTimePerPhase = document.getElementById('chartTotalTime').getContext('2d')
const ctxChartTimePercentage = document.getElementById('chartTimePercentage').getContext('2d')

// Title Counter Actual Time
const spanActualTime = document.getElementById('spanActualTime')
const spanTotalTime = document.getElementById('spanTotalTime')

// Fields Summary
const fieldActualTimeSummary = document.getElementById('fieldActualTimeSummary')
const failureActualProgram = document.getElementById('failureActualProgram')
const failureToDate = document.getElementById('failureToDate')
const fieldTimeToDate = document.getElementById('fieldTimeToDate')
const appraisalCOQActualProgram = document.getElementById('appraisalCOQActualProgram')
const appraisalCOQToDate = document.getElementById('appraisalCOQToDate')
const ratioAFActual = document.getElementById('ratioAFActual')
const ratioAFToDate = document.getElementById('ratioAFToDate')

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
        let totalTimeActualProgram = 0

        // Time per phase actual program
        data.time_per_phase.map(phase => {
            labelsActualTime.push(phase.name)
            minutesPerPhase.push(phase.total_time)
            
            totalTimeActualProgram += phase.total_time
        })

        let resultAppraisalActual = (100 * (data.time_per_phase.find(phase => phase.name == 'Design Review').total_time + data.time_per_phase.find(phase => phase.name == 'Codification Review').total_time) / totalTimeActualProgram).toFixed(2)
        appraisalCOQActualProgram.textContent = resultAppraisalActual

        spanActualTime.textContent = `${totalTimeActualProgram}`
        fieldActualTimeSummary.textContent = `${totalTimeActualProgram}`

        let resultFailureActual = (100 * ((data.time_per_phase.find(phase => phase.name == 'Compilation').total_time + data.time_per_phase.find(phase => phase.name == 'Unit Test').total_time) / totalTimeActualProgram)).toFixed(2)
        failureActualProgram.textContent = resultFailureActual

        ratioAFActual.textContent = (resultAppraisalActual / resultFailureActual).toFixed(2)

        // Time per phase to date
        data.time_per_phase_to_date.map(phase => {
            labelsTotalTime.push(phase.name)
            minutesTotalTime.push(phase.total_time)

            spanTotalTime.textContent = parseInt(spanTotalTime.textContent) + phase.total_time
            totalTime += phase.total_time
        })

        let resultAppraisalToDate = (100 * (data.time_per_phase_to_date.find(phase => phase.name == 'Design Review').total_time + data.time_per_phase_to_date.find(phase => phase.name == 'Codification Review').total_time) / totalTime).toFixed(2)
        appraisalCOQToDate.textContent = resultAppraisalToDate

        fieldTimeToDate.textContent = totalTime

        let resultFailureToDate = (100 * ((data.time_per_phase_to_date.find(phase => phase.name == 'Compilation').total_time + data.time_per_phase_to_date.find(phase => phase.name == 'Unit Test').total_time) / totalTime)).toFixed(2)
        failureToDate.textContent = resultFailureToDate

        ratioAFToDate.textContent = (resultAppraisalToDate / resultFailureToDate).toFixed(2)

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


