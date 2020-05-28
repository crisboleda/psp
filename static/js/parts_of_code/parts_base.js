
// INPUTS
const inputBaseCurrentLines = document.getElementById('baseCurrentLines')
const inputAddedCurrentLines = document.getElementById('addedCurrentLines')
const inputEditedCurrentLines = document.getElementById('editedCurrentLines')
const inputDeletedCurrentLines = document.getElementById('deletedCurrentLines')

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

    data = {
        lines_planned_base: e.target.basePlannedLines.value,
        lines_planned_added: e.target.addedPlannedLines.value,
        lines_planned_edited: e.target.editedPlannedLines.value,
        lines_planned_deleted: e.target.deletedPlannedLines.value,
        lines_current_base: e.target.baseCurrentLines.value,
        lines_current_added: e.target.addedCurrentLines.value,
        lines_current_edited: e.target.editedCurrentLines.value,
        lines_current_deleted: e.target.deletedCurrentLines.value
    }

    apiService.request(e.target.action, data, 'PATCH').then(async (response) => {
        if (response.status == 200){
            location.reload()

        }else {
            let data = await response.json()
            alertErrorEditBaseProgram.classList.remove('d-none')
            
            for (let j = 0; j < data.lines_current_base.length; j++) {
                alertErrorEditBaseProgram.textContent += data.lines_current_base[j]
            }

            setTimeout(() => {
                alertErrorEditBaseProgram.classList.add('d-none')
            }, 3000)
        }
    })

    e.preventDefault()
})