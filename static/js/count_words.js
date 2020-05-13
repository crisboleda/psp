
const inputComments = document.getElementById('id_comments')
const countWords = document.getElementById('count_words_comment_time_log')


inputComments.addEventListener('keydown', (e) =>  {
    countWords.textContent = inputComments.value.length
})