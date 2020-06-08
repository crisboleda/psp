
const apiService = new APIService()

// Canvas Charts
const ctxActualDefects = document.getElementById('chartActualDefects').getContext('2d')
const ctxTotalDefects = document.getElementById('chartTotalDefects').getContext('2d')
const ctxTotalDefectsPercentage = document.getElementById('chartTotalDefectsPercentage').getContext('2d')

// Span total
const spanTotalDefects = document.getElementById('spanTotalDefects')
const spanActualDefects = document.getElementById('spanActualDefects')


apiService.request(`/programs/${idProgram}/data_defects_injected/`, {}, 'GET').then(response => {
    response.json().then(data => setDataGraph(data))
})

function setDataGraph(data) {
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

    createChartBar(ctxActualDefects, labelsActualDefects, numbersActualDefects, "Number of defects injected ACTUAL-PROGRAM")
    createChartBar(ctxTotalDefects, labelsTotalDefects, numbersTotalDefects, "Number of defects injected TO-DATE")
    createChartDoughnut(ctxTotalDefectsPercentage, labelsTotalDefects, numbersPercentage, "Hello world")
}

function calculatePercentage(total, value) {
    return ((100 / total) * value).toFixed(2)
}

function createChartBar(ctx, labels, numbers, title) {
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: title,
                data: numbers,
                backgroundColor: [
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(54, 162, 235, 0.2)',
                    'rgba(255, 206, 86, 0.2)',
                    'rgba(75, 192, 192, 0.2)',
                    'rgba(153, 102, 255, 0.2)',
                    'rgba(255, 159, 64, 0.2)'
                ],
                borderColor: [
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(153, 102, 255, 1)',
                    'rgba(255, 159, 64, 1)'
                ],
                borderWidth: 1.5
            }]
        },
        options: {
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true
                    }
                }]
            }
        }
    })
}


function createChartDoughnut(ctx, labels, numbers, title) {
    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: labels,
            datasets: [{
                label: title,
                data: numbers,
                backgroundColor: [
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(54, 162, 235, 0.2)',
                    'rgba(255, 206, 86, 0.2)',
                    'rgba(75, 192, 192, 0.2)',
                    'rgba(153, 102, 255, 0.2)',
                    'rgba(255, 159, 64, 0.2)'
                ],
                borderColor: [
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(153, 102, 255, 1)',
                    'rgba(255, 159, 64, 1)'
                ],
                borderWidth: 1.5
            }]
        }
    })
}
