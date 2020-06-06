
const paragraphDefectDescription = document.getElementById('modalDefectDescription')
const paragraphDefectSolution = document.getElementById('modalDefectSolution')
const titleModal = document.getElementById('titleDefectModal')

const buttonsOpenModalDetails = document.getElementsByClassName('btnOpenModalDetails')


const setDataModal = (defect) => {
    paragraphDefectDescription.textContent = defect.description
    paragraphDefectSolution.textContent = defect.solution

    console.log(titleModal.textContent)

    titleModal.textContent = `Defect #${defect.number}`
}


for (let i = 0; i < buttonsOpenModalDetails.length; i++) {
    buttonsOpenModalDetails[i].addEventListener('click', (e) => {
        setDataModal(JSON.parse(buttonsOpenModalDetails[i].value))
    })
}
