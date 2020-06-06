
// Loader modal Detail Report
const loaderDetailReport = document.getElementById('loaderDetailReport')
const containerDetailReport = document.getElementById('containerDetailReport')

// loader and content modal delete confirmation report
const loaderDeleteReport = document.getElementById('loaderDeleteReport')
const contentModalDeleteConfirmation = document.getElementById('contentModalDeleteConfirmation')
const modalFooterDeleteConfirmation = document.getElementById('modalFooterDeleteConfirmation')

// Button delete confirmation
const btnDeleteReportConfirmation = document.getElementById('btnDeleteReportConfirmation')

// Button
const btnPreviewDetailReport = document.getElementsByClassName('btnPreviewDetailReport')
const btnDeleteReport = document.getElementsByClassName('btnDeleteReport')

// Inputs modal Detail Report
const modalDetailNameReport = document.getElementById('modalDetailNameReport')
const modalDetailDateReport = document.getElementById('modalDetailDateReport')
const modalDetailObjetiveReport = document.getElementById('modalDetailObjetiveReport')
const modalDetailDescriptionReport = document.getElementById('modalDetailDescriptionReport')
const modalDetailConditionsReport = document.getElementById('modalDetailConditionsReport')
const modalDetailExpectedResultsReport = document.getElementById('modalDetailExpectedResultsReport')
const modalDetailActualResultsReport = document.getElementById('modalDetailActualResultsReport')

const textareaCreateReport = document.getElementsByClassName('text-input-scroll')

var reportDelete = {};


for (let i = 0; i < textareaCreateReport.length; i++) {
    textareaCreateReport[i].addEventListener('keyup', setScrollBottom)
    textareaCreateReport[i].addEventListener('keydown', setScrollBottom)
}


function setScrollBottom(e) {
    e.target.scrollTop = e.target.scrollHeight - e.target.clientHeight
}


for (let i = 0; i < btnPreviewDetailReport.length; i++) {
    btnPreviewDetailReport[i].addEventListener('click', getDetailReport)
}

function getDetailReport(e) {

    containerDetailReport.classList.add('d-none')
    loaderDetailReport.classList.remove('d-none')

    let report = e.target.value
    if (report == undefined) report = e.target.parentElement.value

    report = JSON.parse(report)
    let apiService = new APIService()

    apiService.request(`/reports/${report.idReport}/`, {}, 'GET').then(response => {
        if (response.status == 200){
            loaderDetailReport.classList.add('d-none')
            containerDetailReport.classList.remove('d-none')

            response.json().then(data => {
                console.log(data)
                modalDetailNameReport.textContent = data.name
                modalDetailDateReport.textContent = data.date
                modalDetailObjetiveReport.textContent = data.objetive
                modalDetailDescriptionReport.textContent = data.description
                modalDetailExpectedResultsReport.textContent = data.expect_results
                modalDetailActualResultsReport.textContent = data.current_results
                modalDetailConditionsReport.textContent = data.conditions
            })
        }
    })
}

for (let i = 0; i < btnDeleteReport.length; i++) {
    btnDeleteReport[i].addEventListener('click', showAlertDeleteConfirmation)
}


function showAlertDeleteConfirmation(e) {
    reportDelete = e.target.value
    if (reportDelete == undefined) reportDelete = e.target.parentElement.value
    reportDelete = JSON.parse(reportDelete)

    loaderDeleteReport.classList.add('d-none')
    contentModalDeleteConfirmation.classList.remove('d-none')
    modalFooterDeleteConfirmation.classList.remove('d-none')
}


// Request for delete report
btnDeleteReportConfirmation.addEventListener('click', (e) => {
    let apiService = new APIService()

    contentModalDeleteConfirmation.classList.add('d-none')
    modalFooterDeleteConfirmation.classList.add('d-none')
    loaderDeleteReport.classList.remove('d-none')


    apiService.request(`/reports/${reportDelete.idReport}/`, {}, 'DELETE').then(response => {
        location.reload()
    })
})


