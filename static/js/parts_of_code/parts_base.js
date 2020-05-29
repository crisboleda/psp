
// INPUTS
const inputBaseCurrentLines = document.getElementById('baseCurrentLines')
const inputAddedCurrentLines = document.getElementById('addedCurrentLines')
const inputEditedCurrentLines = document.getElementById('editedCurrentLines')
const inputDeletedCurrentLines = document.getElementById('deletedCurrentLines')

// Form create a new base part
const formCreateBasePart = document.getElementById('formCreateBasePart')

// Alert notification (Danger Error)
const alertError = document.getElementById('alertErrorFormCreateBasePart')

const inputBasePlannedLines = document.getElementById('basePlannedLines')
const inputAddedPlannedLines = document.getElementById('addedPlannedLines')
const inputEditedPlannedtLines = document.getElementById('editedPlannedLines')
const inputDeletedPlannedLines = document.getElementById('deletedPlannedLines')


// Buttons Edit Base program
const buttonsEditBaseProgram = document.getElementsByClassName('btn-edit-base-program')
const modalEditBaseProgram = document.getElementById('editBasePartModal')
const formEditBaseProgram = document.getElementById('form-edit-base-program')
const alertErrorEditBaseProgram = document.getElementById('alertErrorEditBasePart')

const apiService = new APIService()


for (let i = 0; i < buttonsEditBaseProgram.length; i++) {
    buttonsEditBaseProgram[i].addEventListener('click', (e) => {
        setIdFormAction(e)
    })
}


const setIdFormAction = (e) => {
    if (modalEditBaseProgram){
        let basePart = e.target.value
        if (basePart == undefined){
            basePart = e.target.parentElement.value
        }

        basePart = JSON.parse(basePart)

        console.log(basePart)

        formEditBaseProgram.setAttribute('action', `/base_parts/${basePart.id}/update/`)
        
        inputBasePlannedLines.value = basePart.plBase
        inputAddedPlannedLines.value = basePart.plAdded
        inputDeletedPlannedLines.value = basePart.plDeleted
        inputEditedPlannedtLines.value = basePart.plEdited
        
        inputBaseCurrentLines.value = basePart.currentBase
        inputAddedCurrentLines.value = basePart.currentAdded
        inputDeletedCurrentLines.value = basePart.currentDeleted
        inputEditedCurrentLines.value = basePart.currentEdited
        
    }
}


formEditBaseProgram.addEventListener('submit', (e) => {

    let basePlannedLines = e.target.basePlannedLines.value
    let addedPlannedLines = e.target.addedPlannedLines.value
    let editedPlannedLines = e.target.editedPlannedLines.value
    let deletedPlannedLines = e.target.deletedPlannedLines.value
    let baseCurrentLines = e.target.baseCurrentLines.value
    let addedCurrentLines = e.target.addedCurrentLines.value
    let editedCurrentLines = e.target.editedCurrentLines.value
    let deletedCurrentLines = e.target.deletedCurrentLines.value

    validateLines(basePlannedLines, deletedPlannedLines, editedPlannedLines, e, alertErrorEditBaseProgram)
    validateLines(baseCurrentLines, deletedCurrentLines, editedCurrentLines, e, alertErrorEditBaseProgram)

    isLessCero([addedPlannedLines, editedPlannedLines, deletedPlannedLines, baseCurrentLines, addedCurrentLines, editedCurrentLines, deletedCurrentLines], e, alertErrorEditBaseProgram)

    if (basePlannedLines < 1) {
        alertErrorEditBaseProgram.classList.remove('d-none') 
        alertErrorEditBaseProgram.textContent = "The base planned lines can't be less to 1"

        AlertManager.hidden(alertErrorEditBaseProgram)
    }

    let data = {
        lines_planned_base: basePlannedLines,
        lines_planned_added: addedPlannedLines,
        lines_planned_edited: editedPlannedLines,
        lines_planned_deleted: deletedPlannedLines,
        lines_current_base: baseCurrentLines,
        lines_current_added: addedCurrentLines,
        lines_current_edited: editedCurrentLines,
        lines_current_deleted: deletedCurrentLines
    }

    apiService.request(e.target.action, data, 'PATCH').then(async (response) => {
        if (response.status == 200){
            location.reload()

        }else {
            let data = await response.json()
            alertErrorEditBaseProgram.classList.remove('d-none')
            
            for (let j = 0; j < data.lines_current_base.length; j++) {
                alertErrorEditBaseProgram.textContent += data.lines_current_base[j]

                AlertManager.hidden(alertErrorEditBaseProgram)
            }
        }
    })

    e.preventDefault()
})


formCreateBasePart.addEventListener('submit', (e) => {

    let baseLines = parseInt(e.target.id_planning_base_lines.value)
    let deletedLines = parseInt(e.target.id_planning_deleted_lines.value)
    let editedLines = parseInt(e.target.id_planning_edited_lines.value)
    let addedLines = parseInt(e.target.id_planning_added_lines.value)

    validateLines(baseLines, deletedLines, editedLines, e, alertError)
    isLessCero([deletedLines, editedLines, addedLines], e, alertError)

    if (baseLines <= 0){
        alertError.classList.remove('d-none')
        alertError.textContent = "The base lines can't be less or equal to 0"
        AlertManager.hidden(alertError)

        e.preventDefault()

    }
})


function validateLines(baseLines, deletedLines, editedLines, form, alert){
    if ((deletedLines > baseLines) || (editedLines > (baseLines - deletedLines))){
        alert.classList.remove('d-none')
        alert.textContent = "The base lines aren't enough"

        AlertManager.hidden(alert)

        form.preventDefault()
    }
}

function isLessCero(values, form, alert){
    for (let i = 0; i < values.length; i++) {
        if (values[i] < 0){
            form.preventDefault()

            alert.classList.remove('d-none')
            alert.textContent = "The inputs can't be less to 0"

            AlertManager.hidden(alert)
        }
    }
}