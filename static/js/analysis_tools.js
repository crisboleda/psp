

const btnGraphicAnalysis = document.getElementsByClassName('btnGraphicAnalysis')
const ctxGraphic = document.getElementById('canvasGraphicAnalysisTools')

const descriptionGraphic = document.getElementById('descriptionGraphic')
const titleModalGraphic = document.getElementById('titleModalGraphic')

// Loader graphic
const loaderGraphicAnalysisTools = document.getElementById('loaderGraphicAnalysisTools')

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

            switch (graphic.name) {
                
                case 'actual-size':

                    descriptionGraphic.textContent = "Esta grafica muestra el tamaño de cada programa en líneas de código hasta el momento"

                    data.actual_size.map(size => {
                        labels.push(`${size.name.slice(0, 20)}...`)
                        dataGraphic.push(size.total)
                    })

                    CreatorChart.createChartLine(ctxGraphic.getContext('2d'), labels, dataGraphic, "Programs (Actual Size)")
                    break;

                case 'defects-removed':

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

                    CreatorChart.createRadarChart(ctxGraphic.getContext('2d'), labels, datasets, "Defects removed")
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

                    CreatorChart.createRadarChart(ctxGraphic.getContext('2d'), labels, datasets, "Defects Injected")
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
