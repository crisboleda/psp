
class CounterInputValue {

    static showCountValue(input, countWords){

        countWords.textContent = input.value.length

        input.addEventListener('keyup', (e) =>  {
            countWords.textContent = input.value.length
        })

        input.addEventListener('keydown', (e) => {
            countWords.textContent = input.value.length
        })
    }

}