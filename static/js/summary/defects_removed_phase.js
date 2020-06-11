
// Context Charts
const ctxChartActualDefectsRemoved = document.getElementById('chartActualDefectsRemoved')
const ctxChartTotalDefectsRemoved = document.getElementById('chartTotalDefectsRemoved')
const ctxChartTotalDefectsRemovedPercentage = document.getElementById('chartTotalDefectsRemovedPercentage')

// Counters total
const spanActualDefectsRemoved = document.getElementById('spanActualDefectsRemoved')
const spanTotalDefectsRemoved = document.getElementById('spanTotalDefectsRemoved')

// Loader Tab Defects removed
const summaryLoaderDefectsRemoved = document.getElementById('summaryLoaderDefectsRemoved')


apiService.request(`/programs/${idProgram}/data_defects_removed/`, {}, 'GET').then(response => {
    response.json().then(data => {

        summaryLoaderDefectsRemoved.classList.add('d-none')
        summaryLoaderDefectsRemoved.nextElementSibling.classList.remove('d-none')
        
        let labelsActualDefectsRemoved = []
        let dataActualDefectsRemoved = []

        let labelsTotalDefectsRemoved = []
        let dataTotalDefectsRemoved = []

        let dataTotalPercentage = []

        let totalDefects = 0
        
        data.defects_removed.map(defect => {
            labelsActualDefectsRemoved.push(defect.name)
            dataActualDefectsRemoved.push(defect.total)

            spanActualDefectsRemoved.textContent = parseInt(spanActualDefectsRemoved.textContent) + defect.total
        })

        data.defects_removed_to_date.map(defect => {
            labelsTotalDefectsRemoved.push(defect.name)
            dataTotalDefectsRemoved.push(defect.total)

            spanTotalDefectsRemoved.textContent = parseInt(spanTotalDefectsRemoved.textContent) + defect.total
            totalDefects += defect.total
        })

        dataTotalDefectsRemoved.map(value => {
            dataTotalPercentage.push(calculatePercentageDefectsRemoved(value, totalDefects))
        })

        CreatorChart.createChartBar(ctxChartActualDefectsRemoved, labelsActualDefectsRemoved, dataActualDefectsRemoved, "Defects removed ACTUAL-PROGRAM")
        CreatorChart.createChartBar(ctxChartTotalDefectsRemoved, labelsTotalDefectsRemoved, dataTotalDefectsRemoved, "Defects removed TO-DATE")
        CreatorChart.createChartDoughnut(ctxChartTotalDefectsRemovedPercentage, labelsTotalDefectsRemoved, dataTotalPercentage, "sd")
    })
})

function calculatePercentageDefectsRemoved(value, total) {
    return ((100 / total) * value).toFixed(2)
}