
// Loader modal detail PIP
const loaderDetailPIP = document.getElementById('loaderDetailPIP')

// Loader modal delete confirmation
const loaderDeletePIP = document.getElementById('loaderDeletePIP')

// Button modal delete confirmation
const btnDeletePIPConfirmation = document.getElementById('btnDeletePIPConfirmation')

// Content modal delete confirmation
const contentModalDeleteConfirmation = document.getElementById('contentModalDeleteConfirmation')
const modalFooterDeleteConfirmation = document.getElementById('modalFooterDeleteConfirmation')

// Content modal detail PIP
const containerDetailPIP = document.getElementById('containerDetailPIP')

// Items modal detail PIP
const modalDetailNamePIP = document.getElementById('modalDetailNamePIP')
const modalDetailDatePIP = document.getElementById('modalDetailDatePIP')
const modalDetailProblemsPIP = document.getElementById('modalDetailProblemsPIP')
const modalDetailProposalPIP = document.getElementById('modalDetailProposalPIP')
const modalDetailCommentsPIP = document.getElementById('modalDetailCommentsPIP')


// Buttons Preview PIP
const buttonsPreviewPIP = document.getElementsByClassName('btnPreviewDetailPIP')

// Buttons Delete PIP
const buttonsDeletePIP = document.getElementsByClassName('btnDeletePIP')

const textareaFormCreatePIP = document.getElementsByClassName('text-input-scroll')

// PIP will be to delete
var pipWillDelete;


for (let i = 0; i < textareaFormCreatePIP.length; i++) {
    textareaFormCreatePIP[i].addEventListener('keydown', setScrollBottom)
    textareaFormCreatePIP[i].addEventListener('keyup', setScrollBottom)
}


function setScrollBottom(e) {
    e.target.scrollTop = e.target.scrollHeight - e.target.clientHeight
}


for (let i = 0; i < buttonsPreviewPIP.length; i++) {
    buttonsPreviewPIP[i].addEventListener('click', (e) => {

        containerDetailPIP.classList.add('d-none')
        loaderDetailPIP.classList.remove('d-none')

        let pip = e.target.value
        if (pip == undefined) pip = e.target.parentElement.value
        showDetailPIP(JSON.parse(pip)) 
    })
}

function showDetailPIP(pip) {
    let apiService = new APIService()

    apiService.request(`/pips/${pip.idPIP}/`, {}, 'GET').then(response => {

        loaderDetailPIP.classList.add('d-none')
        containerDetailPIP.classList.remove('d-none')

        if (response.status == 200){
            response.json().then(data => {
                modalDetailNamePIP.textContent = data.name
                modalDetailDatePIP.textContent = data.date
                modalDetailProblemsPIP.textContent = data.problems
                modalDetailProposalPIP.textContent = data.proposal
                modalDetailCommentsPIP.textContent = data.comment
            })
        }
    })
}


for (let i = 0; i < buttonsDeletePIP.length; i++) {
    buttonsDeletePIP[i].addEventListener('click', (e) => {

        loaderDeletePIP.classList.add('d-none')
        contentModalDeleteConfirmation.classList.remove('d-none')
        modalFooterDeleteConfirmation.classList.remove('d-none')

        if (e.target.value == undefined){
            pipWillDelete = e.target.parentElement.value
        } else {
            pipWillDelete = e.target.value
        }
    })
}


btnDeletePIPConfirmation.addEventListener('click', (e) => {
    if (pipWillDelete != undefined){
        
        contentModalDeleteConfirmation.classList.add('d-none')
        modalFooterDeleteConfirmation.classList.add('d-none')
        loaderDeletePIP.classList.remove('d-none')

        let apiService = new APIService()
        pipWillDelete = JSON.parse(pipWillDelete)

        apiService.request(`/pips/${pipWillDelete.idPIP}/`, {}, 'DELETE').then(response => {
            location.reload()
        })
    }
})