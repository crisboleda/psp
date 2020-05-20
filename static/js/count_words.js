
class CounterInputValue {

    static showCountValue(input, countWords){
        input.addEventListener('keyup', (e) =>  {
            countWords.textContent = input.value.length
        })

        input.addEventListener('keydown', (e) => {
            countWords.textContent = input.value.length
        })
    }

}