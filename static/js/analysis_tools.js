
const btnGraphicAnalysis = document.getElementsByClassName('btnGraphicAnalysis')
const ctxGraphic = document.getElementById('canvasGraphicAnalysisTools').getContext('2d')


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
    let apiService = new APIService()

    apiService.request(`/users/${graphic.user}/analysis-tools/graphics/`, {}, 'GET').then(response => {
        response.json().then(data => {

            let labels = []
            let dataGraphic = []

            switch (graphic.name) {
                case 'actual-size':
                    data.actual_size.map(size => {
                        labels.push(`${size.name.slice(0, 20)}...`)
                        dataGraphic.push(size.total)
                    })

                    CreatorChart.createChartLine(ctxGraphic, labels, dataGraphic, "Programs (Actual Size)")
                    break;

                default:
                    break;
            }
        })
    })
}