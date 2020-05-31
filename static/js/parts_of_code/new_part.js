

const inputPlannedLinesNewPart = document.getElementById('plannedItemsNewPart')
const inputTypePart = document.getElementById('typeNewPart')
const inputSizeEstimation = document.getElementById('inputSizeEstimation')
const inputLinesEstimation = document.getElementById('inputLinesEstimation')


inputPlannedLinesNewPart.addEventListener('keydown', calculatePlannedLines)
inputPlannedLinesNewPart.addEventListener('keyup', calculatePlannedLines)

inputSizeEstimation.addEventListener('change', calculatePlannedLines)
inputTypePart.addEventListener('change', calculatePlannedLines)


function calculatePlannedLines(){

    let estimation = estimations.find(object => 
        object.type_part.name == inputTypePart.value && 
        object.size_estimation.name == inputSizeEstimation.value
    )
    
    if (inputPlannedLinesNewPart.value != ""){
        inputLinesEstimation.value = (estimation.lines_of_code * parseInt(inputPlannedLinesNewPart.value)).toFixed(2)

    } else {
        inputLinesEstimation.value = "0"
    }
}