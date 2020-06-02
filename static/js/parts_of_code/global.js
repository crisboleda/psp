
const utilUril = new UtilUrl()

const tabMenu1 = document.getElementById('tab1')
const tabMenu2 = document.getElementById('tab2')
const tabMenu3 = document.getElementById('tab3')

const buttonsDeletePart = document.getElementsByClassName('btnDeletePart')
const btnDeletePartConfirmation = document.getElementById('btnDeletePartConfirmation')
var partDelete = {};


let paramUrl = utilUril.getParameterByName('type_part')


switch (paramUrl) {
    case 'reused':
        tabMenu2.checked = true
        break;

    case 'new':
        tabMenu3.checked = true
        break;

    default:
        tabMenu1.checked = true;
}


tabMenu1.addEventListener('click', (e) => utilUril.changeUrlParam('type_part', 'base'))
tabMenu2.addEventListener('click', (e) => utilUril.changeUrlParam('type_part', 'reused'))
tabMenu3.addEventListener('click', (e) => utilUril.changeUrlParam('type_part', 'new'))



for (let i = 0; i < buttonsDeletePart.length; i++) {
    buttonsDeletePart[i].addEventListener('click', (e) => {
        partDelete = e.target.value
        if (partDelete == undefined) partDelete = e.target.parentElement.value

        partDelete = JSON.parse(partDelete)
    })
}


btnDeletePartConfirmation.addEventListener('click', (e) => {
    let myAPIService = new APIService()
    let endpoint = ""

    switch (partDelete.typePart) {
        case 'reused':
            endpoint = `/reused_parts/${partDelete.id}/delete/`
            break;
        
        case 'new':
            endpoint = `/new_parts/${partDelete.id}/delete/`
            break;

        default:
            break;
    }

    if (endpoint != ""){

        Tag.get('id', 'loaderDeletePart').classList.remove('d-none')
        Tag.get('id', 'contentModalDeleteConfirmation').classList.add('d-none')
        Tag.get('id', 'modalFooterDeleteConfirmation').classList.add('d-none')

        myAPIService.request(endpoint, {}, 'DELETE').then(response => {

            if (response.status == 204){
                location.reload()
            } else {
                Tag.get('id', 'loaderDeletePart').classList.add('d-none')
                Tag.get('id', 'contentModalDeleteConfirmation').classList.remove('d-none')
                Tag.get('id', 'contentModalDeleteConfirmation').textContent = "ERROR!!!"
                Tag.get('id', 'modalFooterDeleteConfirmation').classList.remove('d-none')
            }
        })
    }
})



