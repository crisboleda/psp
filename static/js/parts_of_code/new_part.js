

const inputPlannedLinesNewPart = document.getElementById('plannedItemsNewPart')
const inputTypePart = document.getElementById('typeNewPart')
const inputSizeEstimation = document.getElementById('inputSizeEstimation')
const inputLinesEstimation = document.getElementById('inputLinesEstimation')
const buttonsEditNewPart = document.getElementsByClassName('btnEditNewPart')


inputPlannedLinesNewPart.addEventListener('keydown', calculatePlannedLines)
inputPlannedLinesNewPart.addEventListener('keyup', calculatePlannedLines)

inputSizeEstimation.addEventListener('change', calculatePlannedLines)
inputTypePart.addEventListener('change', calculatePlannedLines)

var modalEditNewPart;

for (let i = 0; i < buttonsEditNewPart.length; i++) {
    buttonsEditNewPart[i].addEventListener('click', (e) => setValuesModal(e))
}


function setValuesModal(e){
    let newPart = e.target.value;

    if (newPart == undefined) newPart = e.target.parentElement.value

    let data = JSON.parse(newPart)
    modalEditNewPart = new ModalEditNewPart(data.id, data.name, data.typePart, data.planningMethods, data.sizeEstimation, data.planningLines, data.currentMethods, data.currentLines)
}


Tag.get('id', 'btnEditNewPart').addEventListener('click', () => {

    Tag.get('id', 'loaderEditNewPart').classList.remove('d-none')
    Tag.get('id', 'contentModalBodyNewPart').classList.add('d-none')

    modalEditNewPart.updateNewPart().then(response => {
        if (response.status == 200){
            location.reload()

        } else {

            Tag.get('id', 'loaderEditNewPart').classList.add('d-none')
            Tag.get('id', 'contentModalBodyNewPart').classList.remove('d-none')

            response.json().then(data => {
                setErrorsAttribute(data, 'name_part', modalEditNewPart.inputNameNewPart)
                setErrorsAttribute(data, 'type_part', modalEditNewPart.inputTypeNewPart)
                setErrorsAttribute(data, 'size_estimation', modalEditNewPart.inputSizeEstimationNewPart)
                setErrorsAttribute(data, 'planning_methods', modalEditNewPart.inputPlannedMethodsNewPart)
                setErrorsAttribute(data, 'current_methods', modalEditNewPart.inputCurrentMethodsNewPart)
                setErrorsAttribute(data, 'current_lines', modalEditNewPart.inputCurrentLinesNewPart)
            })
        }
    })
})

function setErrorsAttribute(data, attribute, input) {
    if (data.hasOwnProperty(attribute)){
        
        input.classList.add('is-invalid')
        input.nextElementSibling.textContent = ""

        for (let i = 0; i < data[attribute].length; i++) {
            input.nextElementSibling.textContent += `${data[attribute][i]} \n`
        }
    }
}


function calculatePlannedLines(){

    let estimation = estimations.find(object => 
        object.type_part.name == inputTypePart.value && 
        object.size_estimation.name == inputSizeEstimation.value
    )
    
    if (inputPlannedLinesNewPart.value != ""){
        inputLinesEstimation.value = (estimation.lines_of_code * parseInt(inputPlannedLinesNewPart.value)).toFixed(2)

    } else {
        inputLinesEstimation.value = "0"
    }
}