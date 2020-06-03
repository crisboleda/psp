
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

// Button Update Base Part
const btnUpdateBasePart = document.getElementById('btnUpdateBasePart')

// Buttons Edit Base program
const buttonsEditBaseProgram = document.getElementsByClassName('btn-edit-base-program')
const modalEditBaseProgram = document.getElementById('editBasePartModal')
const formEditBaseProgram = document.getElementById('form-edit-base-program')
const alertErrorEditBaseProgram = document.getElementById('alertErrorEditBasePart')

const apiService = new APIService()


if (buttonsEditBaseProgram){
    for (let i = 0; i < buttonsEditBaseProgram.length; i++) {
        buttonsEditBaseProgram[i].addEventListener('click', (e) => {
            setIdFormAction(e)
        })
    }
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


btnUpdateBasePart.addEventListener('click', (e) => {

    let basePlannedLines = parseInt(Tag.get('id', 'basePlannedLines').value)
    let addedPlannedLines = parseInt(Tag.get('id', 'addedPlannedLines').value)
    let editedPlannedLines = parseInt(Tag.get('id', 'addedPlannedLines').value)
    let deletedPlannedLines = parseInt(Tag.get('id', 'deletedPlannedLines').value)
    let baseCurrentLines = parseInt(Tag.get('id', 'baseCurrentLines').value)
    let addedCurrentLines = parseInt(Tag.get('id', 'addedCurrentLines').value)
    let editedCurrentLines = parseInt(Tag.get('id', 'editedCurrentLines').value)
    let deletedCurrentLines = parseInt(Tag.get('id', 'deletedCurrentLines').value)


    let isValidFirst = validateLines(basePlannedLines, deletedPlannedLines, editedPlannedLines, formEditBaseProgram, alertErrorEditBaseProgram)
    let isValidSecond = validateLines(baseCurrentLines, deletedCurrentLines, editedCurrentLines, formEditBaseProgram, alertErrorEditBaseProgram)
    let isValidLessCero =  isLessCero([addedPlannedLines, editedPlannedLines, deletedPlannedLines, baseCurrentLines, addedCurrentLines, editedCurrentLines, deletedCurrentLines], formEditBaseProgram, alertErrorEditBaseProgram)

    console.log(isValidFirst)
    console.log(isValidSecond)
    console.log(isValidLessCero)

    if (basePlannedLines < 1) {
        alertErrorEditBaseProgram.classList.remove('d-none') 
        alertErrorEditBaseProgram.textContent = "The base planned lines can't be less to 1"

        AlertManager.hidden(alertErrorEditBaseProgram)

    } else if (isValidFirst && isValidSecond && isValidLessCero){

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

        updateBasePart(data, formEditBaseProgram)
    }
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

function updateBasePart(data, form){

    form.classList.add('d-none')

    const loader = Tag.get('id', 'loader-edit-base-part')
    loader.classList.remove('d-none')

    apiService.request(form.getAttribute('action'), data, 'PATCH').then(async (response) => {
        if (response.status == 200){
            location.reload()

        }else {
            let data = await response.json()

            loader.classList.add('d-none')
            form.classList.remove('d-none')
            
            alertErrorEditBaseProgram.classList.remove('d-none')
            
            for (let j = 0; j < data.lines_current_base.length; j++) {
                alertErrorEditBaseProgram.textContent += data.lines_current_base[j]

                AlertManager.hidden(alertErrorEditBaseProgram)
            }
        }
    })
}


function validateLines(baseLines, deletedLines, editedLines, form, alert){

    console.log(baseLines, deletedLines, editedLines)
    

    if ((deletedLines > baseLines) || (editedLines > (baseLines - deletedLines))){
        alert.classList.remove('d-none')
        alert.textContent = "The base lines aren't enough"

        AlertManager.hidden(alert)
        
        if (form != formEditBaseProgram) form.preventDefault()

        return false
    }
    return true
}

function isLessCero(values, form, alert){
    for (let i = 0; i < values.length; i++) {
        if (values[i] < 0){

            if (form != formEditBaseProgram) form.preventDefault()

            alert.classList.remove('d-none')
            alert.textContent = "The inputs can't be less to 0"

            AlertManager.hidden(alert)

            return false
        }
    }
    return true
}


Tag.get('id', 'btnShowTotalLinesBasePart').addEventListener('click', (e) => {
    Tag.get('id', 'btnShowTotalLinesBasePart').classList.add('d-none')
    Tag.get('id', 'btnHiddeTotalLinesBasePart').classList.remove('d-none')
    Tag.get('id', 'totalLinesBaseParts').classList.remove('d-none')
})


Tag.get('id', 'btnHiddeTotalLinesBasePart').addEventListener('click', (e) => {
    Tag.get('id', 'btnHiddeTotalLinesBasePart').classList.add('d-none')
    Tag.get('id', 'btnShowTotalLinesBasePart').classList.remove('d-none')
    Tag.get('id', 'totalLinesBaseParts').classList.add('d-none')
})