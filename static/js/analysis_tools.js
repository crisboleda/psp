

const btnGraphicAnalysis = document.getElementsByClassName('btnGraphicAnalysis')

const descriptionGraphic = document.getElementById('descriptionGraphic')
const titleModalGraphic = document.getElementById('titleModalGraphic')

const ctxGraphic = document.getElementById('canvasGraphicAnalysisTools')

const containerCanvas = document.getElementById('container-canvas')

// Loader graphic
const loaderGraphicAnalysisTools = document.getElementById('loaderGraphicAnalysisTools')

var canvas = null

Chart.defaults.global.defaultFontFamily = "Lato";
Chart.defaults.global.defaultFontSize = 18;


for (let i = 0; i < btnGraphicAnalysis.length; i++) {
    btnGraphicAnalysis[i].addEventListener('click', (e) => {
        let graphic = e.target.value
        if (graphic == undefined) graphic = e.target.parentElement.value

        setDataGraphic(JSON.parse(graphic))
    })
}

function setDataGraphic(graphic) {
    
    // Limpiar las graficas que se ha generado anteriormente
    if (canvas != null){
        canvas.clear()
        canvas.destroy()
    }

    ctxGraphic.classList.add('d-none')
    loaderGraphicAnalysisTools.classList.remove('d-none')

    let apiService = new APIService()
    descriptionGraphic.textContent = ""

    titleModalGraphic.textContent = ((graphic.name).toUpperCase()).replace('-', ' ')

    apiService.request(`/users/${graphic.user}/analysis-tools/graphics/`, {}, 'GET').then(response => {
        response.json().then(data => {

            loaderGraphicAnalysisTools.classList.add('d-none')
            ctxGraphic.classList.remove('d-none')

            let labels = []
            let dataGraphic = []
            let colors = []
            let datasets = []

            console.log(graphic.name)
            console.log(data)

            switch (graphic.name) {
                
                case 'actual-size':
                    descriptionGraphic.textContent = "Esta grafica muestra el tamaño de cada programa en líneas de código hasta el momento"

                    data.actual_size.map(size => {
                        labels.push(`${size.name.slice(0, 20)}...`)
                        dataGraphic.push(size.total)
                    })

                    canvas = CreatorChart.createChartLine(ctxGraphic.getContext('2d'), labels, dataGraphic, "Programs (Actual Size)")
                    break;

                case 'defects-removed':
                    console.log("DEFECTS REMOVED")
                    descriptionGraphic.textContent = "Esta grafica muestra la cantidad de defectos removidos por fase de cada programa"

                    labels = ["Planning", "Design", "Design Review", "Codification", "Codification Review", "Compilation", "Unit Test", "Postmortem"]
                    colors = []
                    datasets = []

                    data.defects_removed.map((defect, counter) => {
                        
                        let backgroundColor, borderColor

                        do {
                            [backgroundColor, borderColor] = generateColorRGBA()
                        } while (colors.findIndex(c => c == backgroundColor) != -1);

                        colors.push(backgroundColor)

                        datasets.push({
                            label: defect.name,
                            data: [defect.planning, defect.design, defect.design_review, defect.codification, defect.codification_review, defect.compilation, defect.unit_test, defect.postmortem],
                            backgroundColor: [backgroundColor],
                            borderColor: borderColor,
                            borderWidth: 1.5
                        })
                    })

                    canvas = CreatorChart.createRadarChart(ctxGraphic.getContext('2d'), labels, datasets, "Defects removed")
                    break;

                case 'defects-injected':

                    descriptionGraphic.textContent = "Esta grafica muestra la cantidad de defectos injectados por fase de cada programa"

                    labels = ["Planning", "Design", "Design Review", "Codification", "Codification Review", "Compilation", "Unit Test", "Postmortem"]
                    colors = []
                    datasets = []
                    
                    data.defects_injected.map(defect => {
                        let backgroundColor, borderColor
                        
                        do {
                            [backgroundColor, borderColor] = generateColorRGBA()
                        } while (colors.findIndex(c => c == backgroundColor) != -1);

                        colors.push(backgroundColor)
                        
                        datasets.push({
                            label: defect.name,
                            data: [defect.planning, defect.design, defect.design_review, defect.codification, defect.codification_review, defect.compilation, defect.unit_test, defect.postmortem],
                            backgroundColor: [backgroundColor],
                            borderColor: borderColor,
                            borderWidth: 1.5
                        })
                    })  

                    canvas = CreatorChart.createRadarChart(ctxGraphic.getContext('2d'), labels, datasets, "Defects Injected")
                    break;

                case 'total-time':
                    descriptionGraphic.textContent = "Esta gráfica muestra el total de tiempo que se ha empleado por cada programa"
                    
                    data.total_time.map((time, counter) => {
                        labels.push(`Program #${counter + 1}`)
                        datasets.push(time.total)
                    })
                    
                    canvas = CreatorChart.createChartBar(ctxGraphic, labels, datasets, "Time total per program (Minutes)")

                    break;
                
                case 'failure-cost-of-quality':
                    descriptionGraphic.textContent = "Esta grafica muesta la falla del costo de calidad el cual se basa en el tiempo gastado en la fase de compilación y de pruebas sobre el total del tiempo. (Si el % del tiempo gastado en estas fases es mayor al 40% se está hay una falla en la calidad)."

                    data.failure_COQ.map((failure, counter) => {
                        labels.push(`Program #${counter + 1}`)
                        datasets.push(failure.total)
                    })

                    canvas = CreatorChart.createChartBar(ctxGraphic, labels, datasets, "Failure Cost of Quality (%)")
                    break;

                case 'appraisal-cost-of-quality':
                    
                    descriptionGraphic.textContent = "Esta grafica muestra que porcentaje estamos dedicando a la prevención, es decir, esta grafica muestra el porcentaje de tiempo gastado en la fase de revisión de diseño y revisión de codigo respecto al tiempo total"

                    data.appraisal_COQ.map((appraisal, counter) => {
                        labels.push(`Program #${counter + 1}`)
                        datasets.push(appraisal.total)
                    })

                    canvas = CreatorChart.createChartBar(ctxGraphic, labels, datasets, "Appraisal Cost of Quality (%)")
                    break;
                
                case 'total-defects':

                descriptionGraphic.textContent = "Esta grafica muestra la cantidad de defectos que se han cometido hasta el momento en cada programa"

                data.total_defects.map((defect, counter) => {
                    labels.push(`Program #${counter + 1}`)
                    datasets.push(defect.total)
                })

                canvas = CreatorChart.createChartLine(ctxGraphic, labels, datasets, "Total defects by program")
                break;
                
                default:
                    break;
            }
        })
    })
}

function generateColorRGBA() {

    let colorRed = Math.random() * (255 - 0) + 0
    let colorGreen = Math.random() * (255 - 0) + 0
    let colorBlue = Math.random() * (255 - 0) + 0

    return [`rgba(${colorRed}, ${colorGreen}, ${colorBlue}, 0.2)`, `rgba(${colorRed}, ${colorGreen}, ${colorBlue}, 1)`]
}
