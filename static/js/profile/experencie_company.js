
// Loader Edit Experencie Company
const loaderExperencieCompany = document.getElementById('loaderExperencieCompany')

// Form Edit Experencie Company
const formEditExperencieCompany = document.getElementById('formEditExperencieCompany')
const footerModalEditExperencieCompany = document.getElementById('footerModalEditExperencieCompany')

// Modal Edit Experencie Company
const modalEditExperencieCompany = document.getElementById('modalEditExperencieCompany')

// Inputs Form Edit Experencie Company
const inputNameCompany = document.getElementById('inputNameCompany')
const inputPositions = document.getElementById('inputPositions')
const inputYearsPosition = document.getElementById('inputYearsPosition')

// Button save changes Form Edit Experencie Company
const btnModalEditExperencieCompany = document.getElementById('btnSaveChangesEditExperencieCompany')
const btnsEditExperencieCompany = document.getElementsByClassName('btnEditExperencieCompany')

// Button delete Exp Company
const btnDeleteExpCompany = document.getElementsByClassName('btnDeleteExpCompany')
const btnDeleteExpCompanyConfirmation = document.getElementById('btnDeleteExpCompanyConfirmation')

// Items Modal delete confirmation
const deleteExpCompanyConfirmation = document.getElementById('deleteExpCompanyConfirmation')
const loaderDeleteExpCompany = document.getElementById('loaderDeleteExpCompany')
const contentModalDeleteConfirmation = document.getElementById('contentModalDeleteConfirmation')
const modalFooterDeleteConfirmation = document.getElementById('modalFooterDeleteConfirmation')

// Items table exp company
const totalItemsExpCompany = document.getElementById('totalItemsExpCompany')


var experencieCompany;
var expCompanyDelete;


for (let i = 0; i < btnsEditExperencieCompany.length; i++) {
    btnsEditExperencieCompany[i].addEventListener('click', (e) => {

        formEditExperencieCompany.classList.add('d-none')
        footerModalEditExperencieCompany.classList.add('d-none')
        loaderExperencieCompany.classList.remove('d-none')

        experencieCompany = e.target.value
        if (experencieCompany == undefined) experencieCompany = e.target.parentElement.value

        getExperencieCompany()
    })
}

function getExperencieCompany() {
    let apiService = new APIService()
    experencieCompany = JSON.parse(experencieCompany)

    apiService.request(`/users/experencie-companies/${experencieCompany.id}/`, {}, 'GET').then(response => {
        response.json().then(data => {

            inputNameCompany.value = data.name_company
            inputPositions.value = data.position_company.name
            inputYearsPosition.value = data.years_position

            loaderExperencieCompany.classList.add('d-none')
            formEditExperencieCompany.classList.remove('d-none')
            footerModalEditExperencieCompany.classList.remove('d-none')
        })
    })
}


btnModalEditExperencieCompany.addEventListener('click', (e) => {
    
    let apiService = new APIService()

    formEditExperencieCompany.classList.add('d-none')
    footerModalEditExperencieCompany.classList.add('d-none')
    loaderExperencieCompany.classList.remove('d-none')

    let body = {
        name_company: inputNameCompany.value,
        position_company: inputPositions.value,
        years_position: inputYearsPosition.value
    }

    apiService.request(`/users/experencie-companies/${experencieCompany.id}/`, body, 'PATCH').then(response => {
        if (response.status == 200){
            location.reload()
        }
    })

})


for (let i = 0; i < btnDeleteExpCompany.length; i++) {
    btnDeleteExpCompany[i].addEventListener('click', (e) => {
        expCompanyDelete = e.target.value
        if (expCompanyDelete == undefined) expCompanyDelete = e.target.parentElement.value

        expCompanyDelete = JSON.parse(expCompanyDelete)
    })
}


btnDeleteExpCompanyConfirmation.addEventListener('click', (e) => {

    contentModalDeleteConfirmation.classList.add('d-none')
    modalFooterDeleteConfirmation.classList.add('d-none')
    loaderDeleteExpCompany.classList.remove('d-none')

    let apiService = new APIService()

    apiService.request(`/users/experencie-companies/${expCompanyDelete.idExperencie}/`, {}, 'DELETE').then(response => {
        if (response.status == 204){
            document.body.classList.remove('modal-open')
            document.body.lastChild.remove()
            
            deleteExpCompanyConfirmation.classList.remove('show')
            deleteExpCompanyConfirmation.classList.add('d-none')

            let itemTable = totalItemsExpCompany.childNodes[expCompanyDelete.numberRow]
            totalItemsExpCompany.removeChild(itemTable)
        }
    })
})

