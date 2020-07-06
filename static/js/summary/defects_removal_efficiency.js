

const ctxActualProgram = document.getElementById('chartDefectsRemovalEfficiencyActual').getContext('2d')
const ctxDataToDate = document.getElementById('chartDefectsRemovalEfficiencyToDate').getContext('2d')

const containerGraphics = document.getElementById('sectionDefectsRemovalEfficiency')

// Loader
const loaderDefectsRemovalEfficiency = document.getElementById('summaryLoaderDefectsRemovalEfficiency')

const tableBodyDRL = document.getElementById('tableBodyDRL')


// Establecemos los datos haciendo una llamada al servidor
async function setDataInGraphics() {
    let apiService = new APIService()

    let leverageActual = []
    let leverageToDate = []

    let defectsRemovalEfficiencyActual = { labels: [], data: [] }
    let defectsRemovalEfficiencyToDate = { labels: [], data: [] }
    
    const responseTimePerPhase = await apiService.request(`/programs/${idProgram}/data_time_per_phase/`, {}, 'GET')
    const dataTimePerPhase = await responseTimePerPhase.json()

    const responseDefectsRemoved = await apiService.request(`/programs/${idProgram}/data_defects_removed/`, {}, 'GET')
    const dataDefectsRemovedPerPhase = await responseDefectsRemoved.json()

    loaderDefectsRemovalEfficiency.classList.add('d-none')
    containerGraphics.classList.remove('d-none')

    dataDefectsRemovedPerPhase.defects_removed.map(phase => {
        let timePhase = dataTimePerPhase.time_per_phase.find(obj => obj.name == phase.name)

        defectsRemovalEfficiencyActual.labels.push(phase.name)
        defectsRemovalEfficiencyActual.data.push(parseInt(60 * convertZeroIsNaN(phase.total / timePhase.total_time)))
    })

    // Obtengo los leverage del programa actual
    leverageActual.push(calculateLeverage(defectsRemovalEfficiencyActual, 'Design Review'))
    leverageActual.push(calculateLeverage(defectsRemovalEfficiencyActual, 'Codificacion Review'))
    leverageActual.push(calculateLeverage(defectsRemovalEfficiencyActual, 'Compilation'))

    dataDefectsRemovedPerPhase.defects_removed_to_date.map(phase => {
        let timePhase = dataTimePerPhase.time_per_phase_to_date.find(obj => obj.name == phase.name)

        defectsRemovalEfficiencyToDate.labels.push(phase.name)
        defectsRemovalEfficiencyToDate.data.push(parseInt(60 * convertZeroIsNaN(phase.total / timePhase.total_time)))
    })

    // Obtengo los leverage hasta la fecha actual
    leverageToDate.push(calculateLeverage(defectsRemovalEfficiencyToDate, 'Design Review'))
    leverageToDate.push(calculateLeverage(defectsRemovalEfficiencyToDate, 'Codification Review'))
    leverageToDate.push(calculateLeverage(defectsRemovalEfficiencyToDate, 'Compilation'))

    setDataLeverageInTable(leverageActual, leverageToDate)

    CreatorChart.createChartBar(ctxActualProgram, defectsRemovalEfficiencyActual.labels, defectsRemovalEfficiencyActual.data, "Defects/Hr. ACTUAL-PROGRAM")
    CreatorChart.createChartBar(ctxDataToDate, defectsRemovalEfficiencyToDate.labels, defectsRemovalEfficiencyToDate.data, "Defects/Hr. TO-DATE")
}

// Obtengo el dato de cada fase por el indice de una lista para buscalo en la otra lista
function calculateLeverage(defectsRemovalEfficiency, phase) {
    return {
        name: phase,
        result: convertZeroIsNaN(defectsRemovalEfficiency.data[defectsRemovalEfficiency.labels.findIndex(obj => obj == phase)] / defectsRemovalEfficiency.data[defectsRemovalEfficiency.labels.findIndex(obj => obj == 'Unit Test')])
    }
}


// Establesco los leverage en la tabla
function setDataLeverageInTable(leverageActual, leverageToDate) {

    leverageActual.forEach((leverage, counter) => {
        let tr = document.createElement('tr')

        createTd(tr, `DRL (${leverage.name}/Unit Test)`)
        createTd(tr, leverage.result)
        createTd(tr, leverageToDate[counter].result)

        tableBodyDRL.appendChild(tr)
    });
}

function createTd(tr, value) {
    let td = document.createElement('td')
    td.textContent = value
    tr.appendChild(td)
}


// Si un data es NaN retorno un cero, de lo contrario retorno el mismo número
function convertZeroIsNaN(value) {
    return isNaN(value) ? 0 : value
}


setDataInGraphics()
