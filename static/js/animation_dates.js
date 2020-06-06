const btnDownDates = document.getElementsByClassName('btn-dates-down')
const btnUpDates = document.getElementsByClassName('btn-dates-up')


for (let i = 0; i < btnDownDates.length; i++) {
    btnDownDates[i].addEventListener('click', (e) => {

        e.target.classList.add('d-none')
        e.target.nextElementSibling.classList.remove('d-none')

        let children = e.target.parentNode.parentNode.parentNode.children

        for (let x = 0; x < children.length; x++){
            if (children[x].classList.contains('d-none')){
                children[x].classList.remove('d-none')
            }
        }
    })
}

for (let m = 0; m < btnUpDates.length; m++){
    btnUpDates[m].addEventListener('click', (e) => {

        e.target.classList.add('d-none')
        e.target.previousElementSibling.classList.remove('d-none')

        let children = e.target.parentNode.parentNode.parentNode.children

        for (let j = 0; j < children.length; j++){
            if (j != 0) children[j].classList.add('d-none')
        }
    })
}