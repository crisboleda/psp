

const textareaCreateReport = document.getElementsByClassName('text-input-scroll')


for (let i = 0; i < textareaCreateReport.length; i++) {
    console.log(textareaCreateReport[i])
    textareaCreateReport[i].addEventListener('keyup', setScrollBottom)
    textareaCreateReport[i].addEventListener('keydown', setScrollBottom)
}


function setScrollBottom(e) {
    e.target.scrollTop = e.target.scrollHeight - e.target.clientHeight
}