
// Buttons
const btnEditExperencieYears = document.getElementById('btnEditExperencieYears')
const btnModalEditExperienceYears = document.getElementById('btnModalEditExperienceYears')

// Loader modal
const loaderFormEditExperencie = document.getElementById('loaderFormEditExperencie')

// Inputs
const containerInputs = document.getElementById('FormEditExperencieYear')

const inputYearsDevelopment = document.getElementById('inputYearsDevelopment')
const inputYearsConfiguration = document.getElementById('inputYearsConfiguration')
const inputYearsIntegration = document.getElementById('inputYearsIntegration')
const inputYearRequirements = document.getElementById('inputYearRequirements')
const inputYearsDesign = document.getElementById('inputYearsDesign')
const inputYearsTesting = document.getElementById('inputYearsTesting')
const inputYearsSupport = document.getElementById('inputYearsSupport')

const inputsYears = [inputYearsDevelopment, inputYearsConfiguration, inputYearsIntegration, inputYearRequirements, inputYearsDesign, inputYearsTesting, inputYearsSupport]

// Model
var profile = {}


btnEditExperencieYears.addEventListener('click', (e) => {
    profile = e.target.value
    if (profile == undefined) profile = e.target.parentElement.value

    profile = JSON.parse(profile)

    let apiService = new APIService()

    apiService.request(`/users/profiles/${profile.id}/total-experencie/`, {}, 'GET').then(response => {
        if (response.status == 200){
            loaderFormEditExperencie.classList.add('d-none')
            containerInputs.classList.remove('d-none')

            response.json().then(data => {
                inputYearsDevelopment.value = data.years_development
                inputYearsConfiguration.value = data.years_configuration
                inputYearsIntegration.value = data.years_integration
                inputYearRequirements.value = data.years_requirements
                inputYearsDesign.value = data.years_design
                inputYearsTesting.value = data.years_tests
                inputYearsSupport.value = data.years_support
            })
        }
    })
})


btnModalEditExperienceYears.addEventListener('click', async (e) => {

    if (validateInputLessCero() == -1){
        containerInputs.classList.add('d-none')
        loaderFormEditExperencie.classList.remove('d-none')
    
        data = {
            years_development: inputYearsDevelopment.value,
            years_configuration: inputYearsConfiguration.value,
            years_integration: inputYearsIntegration.value,
            years_requirements: inputYearRequirements.value,
            years_design: inputYearsDesign.value,
            years_tests: inputYearsTesting.value,
            years_support: inputYearsSupport.value
        }
    
        let apiService = new APIService()
        let response = await apiService.request(`/users/profiles/${profile.id}/total-experencie/`, data, 'PATCH')
    
        if (response.status == 200){
            location.reload()
        }
    }
})


function validateInputLessCero() {
    return inputsYears.findIndex(input => input.value == "" || parseInt(input.value) < 0 || parseInt(input.value) > 100)
}


function verifyInput(e) {
    let input = e.target

    if (input.value == "") {
        input.classList.add('is-invalid')
        input.nextElementSibling.textContent = "The value can't be Empty"

    } else if (parseInt(input.value) < 0) {
        input.classList.add('is-invalid')
        input.nextElementSibling.textContent = "The value can't be less to 0"
    
    } else if (parseInt(input.value) > 100){
        input.classList.add('is-invalid')
        input.nextElementSibling.textContent = "The value can't be higher to 100"
    
    } else {
        input.nextElementSibling.textContent = ""
        input.classList.remove('is-invalid')
    }
}


inputsYears.map(input => {
    input.addEventListener('keyup', verifyInput)
    input.addEventListener('keydown', verifyInput)
})

