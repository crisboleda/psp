
const input = document.getElementById('id_comments')
const countWords = document.getElementById('count_words_comment_time_log')


input.addEventListener('keyup', (e) =>  {
    countWords.textContent = input.value.length
})