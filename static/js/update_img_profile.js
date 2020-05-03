

const containerUpdateImage = document.getElementById('container-update-img-profile')
const containerImageProfile = document.getElementById('container-img-profile')
const contentMainImageProfile = document.getElementById('content-img-profile')


// Ese evento hace que cuando el maouse pase por encima del elemento suceda la siguiente logica:
containerImageProfile.addEventListener('mouseenter', () => {
    containerImageProfile.classList.add('d-none')

    containerUpdateImage.classList.remove('d-none')
    containerUpdateImage.classList.add('d-block')
})

contentMainImageProfile.addEventListener('mouseleave', () => {
    containerUpdateImage.classList.add('d-none')
    containerUpdateImage.classList.remove('d-block')

    containerImageProfile.classList.remove('d-none')
})


const containerFile = document.getElementById('customFile')
containerFile.children[0].addEventListener('change', (e) => {
    console.log(e.target.value.slice(12, e.target.value.length))
    containerFile.children[1].textContent = e.target.value.slice(12, e.target.value.length)
})







