

const textareaFormCreatePIP = document.getElementsByClassName('text-input-scroll')


for (let i = 0; i < textareaFormCreatePIP.length; i++) {
    textareaFormCreatePIP[i].addEventListener('keydown', setScrollBottom)
    textareaFormCreatePIP[i].addEventListener('keyup', setScrollBottom)
}


function setScrollBottom(e) {
    e.target.scrollTop = e.target.scrollHeight - e.target.clientHeight
}