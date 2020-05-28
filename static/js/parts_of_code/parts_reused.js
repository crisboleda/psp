
const btnEditReusedPart = document.getElementById('btnEditReusedPart')
const formEditReusedPart = document.getElementById('form-edit-reused-part')

const inputReusedBaseLines = document.getElementById('reusedBaseLines')
const inputReusedCurrentLines = document.getElementById('reusedCurrentLines')


btnEditReusedPart.addEventListener('click', (e) => {
    let reusedPart = e.target.value

    if (reusedPart == undefined){
        reusedPart = e.target.parentElement.value
    }

    reusedPart = JSON.parse(reusedPart)

    inputReusedBaseLines.value = reusedPart.plannedLines
    inputReusedCurrentLines.value = reusedPart.currentLines

    formEditReusedPart.setAttribute('action', `/reused_parts/${reusedPart.id}/update/`)
})


formEditReusedPart.addEventListener('submit', (e) => {

    let apiService = new APIService()

    let data = {
        planned_lines: inputReusedBaseLines.value,
        current_lines: inputReusedCurrentLines.value
    }

    apiService.request(e.target.action, data, 'PATCH').then(async (response) => {
        if (response.status == 200){
            location.reload()
        }
    })

    e.preventDefault()
})
