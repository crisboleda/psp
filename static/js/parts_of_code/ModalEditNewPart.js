

class ModalEditNewPart {

    inputNameNewPart = document.getElementById('nameNewPart')
    inputTypeNewPart = document.getElementById('typeNewPart')
    inputPlannedMethodsNewPart = document.getElementById('plannedMethodsNewPart')
    inputSizeEstimationNewPart = document.getElementById('sizeEstimationNewPart')
    inputLinesEstimationNewPart = document.getElementById('linesEstimationNewPart')
    inputCurrentMethodsNewPart = document.getElementById('currentMethodsNewPart')
    inputCurrentLinesNewPart = document.getElementById('currentLinesNewPart')
    idNewPart = 0

    constructor(id, name, type, plannedMethods, sizeEstimation, linesEstimation, currentMethods, currentLines){
        this.idNewPart = id
        this.inputNameNewPart.value = name
        this.inputTypeNewPart.value = type
        this.inputPlannedMethodsNewPart.value = plannedMethods
        this.inputSizeEstimationNewPart.value = sizeEstimation
        this.inputLinesEstimationNewPart.value = linesEstimation
        this.inputCurrentMethodsNewPart.value = currentMethods
        this.inputCurrentLinesNewPart.value = currentLines

        // Set Events
        this.inputPlannedMethodsNewPart.addEventListener('keyup', this.calculateLinesEstimation.bind(this))
        this.inputPlannedMethodsNewPart.addEventListener('keydown', this.calculateLinesEstimation.bind(this))
        this.inputTypeNewPart.addEventListener('change', this.calculateLinesEstimation.bind(this))
        this.inputSizeEstimationNewPart.addEventListener('change', this.calculateLinesEstimation.bind(this))
    }

    calculateLinesEstimation(){

        console.log(this.inputTypeNewPart)

        let estimation = estimations.find(object => 
            object.type_part.name == this.inputTypeNewPart.value && 
            object.size_estimation.name == this.inputSizeEstimationNewPart.value
        )
        
        if (this.inputPlannedMethodsNewPart.value != ""){
            this.inputLinesEstimationNewPart.value = (estimation.lines_of_code * parseInt(this.inputPlannedMethodsNewPart.value)).toFixed(2)

        }else {
            this.inputLinesEstimationNewPart.value = "0"
        }
    }

    async updateNewPart(){

        let body = {
            name_part: this.inputNameNewPart.value,
            type_part: this.inputTypeNewPart.value,
            size_estimation: this.inputSizeEstimationNewPart.value,
            planning_methods: this.inputPlannedMethodsNewPart.value,
            current_methods: this.inputCurrentMethodsNewPart.value,
            current_lines: this.inputCurrentLinesNewPart.value
        }

        return await apiService.request(`/new_parts/${this.idNewPart}/update/`, body, 'PATCH')
    }

}