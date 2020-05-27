
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
        let idBaseProgram = e.target.value
        if (idBaseProgram == undefined){
            idBaseProgram = e.target.parentElement.value
        }
        formEditBaseProgram.setAttribute('action', `/base_parts/${idBaseProgram}/update/`)
    }
}


formEditBaseProgram.addEventListener('submit', (e) => {

    data = {
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