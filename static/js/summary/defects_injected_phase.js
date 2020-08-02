
const apiService = new APIService()

// Canvas Charts
const ctxActualDefects = document.getElementById('chartActualDefects').getContext('2d')
const ctxTotalDefects = document.getElementById('chartTotalDefects').getContext('2d')
const ctxTotalDefectsPercentage = document.getElementById('chartTotalDefectsPercentage').getContext('2d')

// Span total
const spanTotalDefects = document.getElementById('spanTotalDefects')
const spanActualDefects = document.getElementById('spanActualDefects')

// Loader Tab defects Injected
const summaryLoaderDefectsInjected = document.getElementById('summaryLoaderDefectsInjected')


apiService.request(`/programs/${idProgram}/data_defects_injected/`, {}, 'GET').then(response => {
    response.json().then(data => setDataGraph(data))
})

function setDataGraph(data) {

    summaryLoaderDefectsInjected.classList.add('d-none')
    summaryLoaderDefectsInjected.nextElementSibling.classList.remove('d-none')

    let numbersTotalDefects = []
    let numbersActualDefects = []
    let numbersPercentage = []

    let labelsTotalDefects = []
    let labelsActualDefects = []

    data.defects_injected.map(defect => {
        spanActualDefects.textContent = parseInt(spanActualDefects.textContent) + defect.total
        labelsActualDefects.push(defect.name)
        numbersActualDefects.push(defect.total)
    })

    data.defects_to_date.map(defect => {
        spanTotalDefects.textContent = parseInt(spanTotalDefects.textContent) + defect.total
        labelsTotalDefects.push(defect.name)
        numbersTotalDefects.push(defect.total)
    })

    numbersTotalDefects.map(number => {
        let total = parseInt(spanTotalDefects.textContent)
        numbersPercentage.push(calculatePercentage(total, number))
    })

    CreatorChart.createChartBar(ctxActualDefects, labelsActualDefects, numbersActualDefects, "Number of defects injected ACTUAL-PROGRAM")
    CreatorChart.createChartBar(ctxTotalDefects, labelsTotalDefects, numbersTotalDefects, "Number of defects injected TO-DATE")
    CreatorChart.createChartDoughnut(ctxTotalDefectsPercentage, labelsTotalDefects, numbersPercentage, "Hello world")
}

function calculatePercentage(total, value) {
    return ((100 / total) * value).toFixed(2)
}

