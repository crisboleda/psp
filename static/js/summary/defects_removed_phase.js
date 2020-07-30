
// Context Charts
const ctxChartActualDefectsRemoved = document.getElementById('chartActualDefectsRemoved')
const ctxChartTotalDefectsRemoved = document.getElementById('chartTotalDefectsRemoved')
const ctxChartTotalDefectsRemovedPercentage = document.getElementById('chartTotalDefectsRemovedPercentage')

// Counters total
const spanActualDefectsRemoved = document.getElementById('spanActualDefectsRemoved')
const spanTotalDefectsRemoved = document.getElementById('spanTotalDefectsRemoved')

// Fields Summary
const fieldTotalDefectsKLOC = document.getElementById('fieldTotalDefectsKLOC')
const fieldTotalDefectsPlan = document.getElementById('fieldTotalDefectsPlan')
const fieldTotalDefectsUTPlan = document.getElementById('fieldTotalDefectsUTPlan')
const fieldTotalDefectsUT = document.getElementById('fieldTotalDefectsUT')
const fieldTotalDefectsToDate = document.getElementById('fieldTotalDefectsToDate')
const yieldSummaryActualProgram = document.getElementById('yieldSummaryActualProgram')
const yieldSummaryToDate = document.getElementById('yieldSummaryToDate')


// Loader Tab Defects removed
const summaryLoaderDefectsRemoved = document.getElementById('summaryLoaderDefectsRemoved')


apiService.request(`/programs/${idProgram}/data_defects_removed/`, {}, 'GET').then(response => {
    response.json().then(data => {
        console.log(data)
        summaryLoaderDefectsRemoved.classList.add('d-none')
        summaryLoaderDefectsRemoved.nextElementSibling.classList.remove('d-none')
        
        let labelsActualDefectsRemoved = []
        let dataActualDefectsRemoved = []

        let labelsTotalDefectsRemoved = []
        let dataTotalDefectsRemoved = []

        let dataTotalPercentage = []

        let totalDefects = 0
        let totalDefectsActualProgram = 0
        let totalDefectsBeforeCompileActual = 0
        let totalDefectsBeforeCompileToDate = 0
        
        
        // Estructurar y manipulación de los defectos removidos del programa actual
        data.defects_removed.map(defect => {
            labelsActualDefectsRemoved.push(defect.name)
            dataActualDefectsRemoved.push(defect.total)

            if (defect.name != 'Compilation' && defect.name != 'Unit Test' && defect.name != 'Postmortem'){
                totalDefectsBeforeCompileActual += defect.total
            }

            totalDefectsActualProgram += defect.total
        })

        spanActualDefectsRemoved.textContent = `${totalDefectsActualProgram}`
        fieldTotalDefectsKLOC.textContent = `${convertToZeroIsNaN((1000 * (totalDefectsActualProgram / parseInt(fieldTotalDefectsKLOC.getAttribute('add-modified-lines')))).toFixed(2))}`
        //------------------->

        // Estructurar y manipulación de los defectos removidos a la fecha actual
        data.defects_removed_to_date.map(defect => {
            labelsTotalDefectsRemoved.push(defect.name)
            dataTotalDefectsRemoved.push(defect.total)

            if (defect.name != 'Compilation' && defect.name != 'Unit Test' && defect.name != 'Postmortem'){
                totalDefectsBeforeCompileToDate += defect.total
            }

            totalDefects += defect.total
        })

        spanTotalDefectsRemoved.textContent = totalDefects

        fieldTotalDefectsPlan.textContent = `${convertToZeroIsNaN((1000 * (totalDefects / parseInt(fieldTotalDefectsPlan.getAttribute('lines')))).toFixed(2))}`
        fieldTotalDefectsUTPlan.textContent = `${convertToZeroIsNaN((1000 * (data.defects_removed_to_date.find(defect => defect.name == 'Unit Test').total / parseInt(fieldTotalDefectsUTPlan.getAttribute('data-lines')))).toFixed(2))}`
        fieldTotalDefectsUT.textContent = `${convertToZeroIsNaN((1000 * (data.defects_removed_to_date.find(defect => defect.name == 'Unit Test').total / parseInt(fieldTotalDefectsUT.getAttribute('lines')))).toFixed(2))}`
        fieldTotalDefectsToDate.textContent = `${convertToZeroIsNaN((1000 * (totalDefects / parseInt(fieldTotalDefectsToDate.getAttribute('lines')))).toFixed(2))}`
        //------------------->

        calculateYieldSummary(totalDefectsBeforeCompileActual, totalDefectsBeforeCompileToDate)

        // Calcular el porcentaje de los defectos removidos a la fecha actual
        dataTotalDefectsRemoved.map(value => {
            dataTotalPercentage.push(calculatePercentageDefectsRemoved(value, totalDefects))
        })

        // Estructurar información en las graficas.
        CreatorChart.createChartBar(ctxChartActualDefectsRemoved, labelsActualDefectsRemoved, dataActualDefectsRemoved, "Defects removed ACTUAL-PROGRAM")
        CreatorChart.createChartBar(ctxChartTotalDefectsRemoved, labelsTotalDefectsRemoved, dataTotalDefectsRemoved, "Defects removed TO-DATE")
        CreatorChart.createChartDoughnut(ctxChartTotalDefectsRemovedPercentage, labelsTotalDefectsRemoved, dataTotalPercentage, "sd")
    })
})

function calculatePercentageDefectsRemoved(value, total) {
    return ((100 / total) * value).toFixed(2)
}


function calculateYieldSummary(defectsRemovedBeforeCompileActual, defectsRemovedBeforeCompileToDate) {
    apiService.request(`/programs/${idProgram}/data_defects_injected/`, {}, 'GET').then(response => {
        response.json().then(data => {
            
            let defectsInjectedBeforeCompileActual = 0
            let defectsInjectedBeforeCompileToDate = 0

            data.defects_injected.map(defect => {
                if (defect.name != 'Compilation' && defect.name != 'Unit Test' && defect.name != 'Postmortem'){
                    defectsInjectedBeforeCompileActual += defect.total
                }
            })

            data.defects_to_date.map(defect => {
                if (defect.name != 'Compilation' && defect.name != 'Unit Test' && defect.name != 'Postmortem'){
                    defectsInjectedBeforeCompileToDate += defect.total
                }
            })
            
            let resultYieldActual = convertToZeroIsNaN((100 * (defectsRemovedBeforeCompileActual / defectsInjectedBeforeCompileActual)).toFixed(2))
            let resultYieldToDate = convertToZeroIsNaN((100 * (defectsRemovedBeforeCompileToDate / defectsInjectedBeforeCompileToDate)).toFixed(2))

            yieldSummaryActualProgram.textContent = resultYieldActual
            yieldSummaryToDate.textContent = resultYieldToDate
        })
    })
}


function convertToZeroIsNaN(value) {
    return isNaN(value) || value == Infinity ? 0 : value
}