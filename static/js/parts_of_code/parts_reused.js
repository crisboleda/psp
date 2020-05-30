
const buttonsEditReusedPart = document.getElementsByClassName('buttonsEditReusedPart')
const formEditReusedPart = document.getElementById('form-edit-reused-part')

const formCreateReusedPart = Tag.get('id', 'form-create-reused-part')

const alertErrorCreateReusedPart = Tag.get('id', 'alert-error-create-reused-part')
const alertErrorEditeReusedPart = Tag.get('id', 'alertEditReusedPart')

const inputReusedBaseLines = document.getElementById('reusedBaseLines')
const inputReusedCurrentLines = document.getElementById('reusedCurrentLines')


if (buttonsEditReusedPart) {
    for (let i = 0; i < buttonsEditReusedPart.length; i++) {
        buttonsEditReusedPart[i].addEventListener('click', (e) => {
            let reusedPart = e.target.value
    
            if (reusedPart == undefined){
                reusedPart = e.target.parentElement.value
            }
        
            reusedPart = JSON.parse(reusedPart)
            console.log(reusedPart)
        
            inputReusedBaseLines.value = reusedPart.plannedLines
            inputReusedCurrentLines.value = reusedPart.currentLines
        
            formEditReusedPart.setAttribute('action', `/reused_parts/${reusedPart.id}/update/`)
        })
    }
}

formCreateReusedPart.addEventListener('submit', (e) => {
    
    let linesPlanning = e.target.id_lines_planning.value
    let linesCurrent = e.target.id_lines_current.value

    if(!validateLinesReusedPart(linesPlanning, linesCurrent, alertErrorCreateReusedPart)){
        e.preventDefault()
    }
    
})


formEditReusedPart.addEventListener('submit', (e) => {
    e.preventDefault()
    let apiService = new APIService()

    let data = {
        planned_lines: inputReusedBaseLines.value,
        current_lines: inputReusedCurrentLines.value
    }

    if (validateLinesReusedPart(inputReusedBaseLines.value, inputReusedCurrentLines.value, alertErrorEditeReusedPart)){

        Tag.get('id', 'loaderEditReusedPart').classList.remove('d-none')
        formEditReusedPart.classList.add('d-none')

        apiService.request(e.target.action, data, 'PATCH').then(async (response) => {
            if (response.status == 200){
                location.reload()
            }
        })
    }
})


function validateLinesReusedPart(linesPlanning, linesCurrent, alert) {
    if (linesPlanning == "" || parseInt(linesPlanning) <= 0 || parseInt(linesCurrent) < 0 || parseInt(linesCurrent) > 2000000000 || parseInt(linesPlanning) > 2000000000){

        alert.classList.remove('d-none')

        if (linesPlanning == ""){
            alert.textContent = "The planning lines can't be empty"

        } else if (parseInt(linesPlanning) <= 0){
            alert.textContent = "The planning lines can't be less or equals than 0"

        } else if (parseInt(linesCurrent)){
            alert.textContent = "The current lines can't be less than 0"

        } else if (parseInt(linesCurrent) > 2000000000 || parseInt(linesPlanning) > 2000000000){
            alert.textContent = "The lines can't be gretter than 2000000000"
        }

        setTimeout(() => {
            alert.classList.add('d-none')
        }, 3500)

        return false
    }
    return true
}
