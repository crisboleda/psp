
const iconHelpInputCousingDefect = document.getElementById('tip-help-cousing-input')
const inputCousingDefect = document.getElementById('input-cousing')
const containerHelpTipCousingDefect = document.getElementById('tip-help-cousing-defect')


iconHelpInputCousingDefect.addEventListener('mouseenter', (e) => {
    inputCousingDefect.classList.add('d-none')
    containerHelpTipCousingDefect.classList.remove('d-none')
})

iconHelpInputCousingDefect.addEventListener('mouseleave', (e) => {
    inputCousingDefect.classList.remove('d-none')
    containerHelpTipCousingDefect.classList.add('d-none')
})


