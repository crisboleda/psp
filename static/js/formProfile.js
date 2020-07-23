
// Buttons
const btnEditProfile = document.getElementById('btnEditProfile')
const btnSaveProfile = document.getElementById('btnSaveProfile')
const btnCancelProfile = document.getElementById('btnCancelProfile')

const inputsProfile = document.getElementsByClassName('input-profile')


if (btnEditProfile){
    btnEditProfile.addEventListener('click', () => {
        for (let i = 0; i < inputsProfile.length; i++) {
            inputsProfile[i].removeAttribute('disabled')
        }
    
        btnEditProfile.classList.add('d-none')
        btnSaveProfile.classList.remove('d-none')
        btnCancelProfile.classList.remove('d-none')
    })
}

if (btnCancelProfile){
    btnCancelProfile.addEventListener('click', () => {

        for (let i = 0; i < inputsProfile.length; i++) {
            inputsProfile[i].setAttribute('disabled', true)
        }
    
        btnEditProfile.classList.remove('d-none')
    
        btnSaveProfile.classList.add('d-none')
        btnCancelProfile.classList.add('d-none')
    })
}

