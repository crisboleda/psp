

const calendarEle = document.getElementById('calendar')

const loaderDatesCalendar = document.getElementById('loaderDatesCalendar')
const containerCalendar = document.getElementById('containerCalendar')


let apiService = new APIService()
var events = []

apiService.request('/dates-delivery/', {}, 'GET').then(response => response.json().then(data => {
    
    loaderDatesCalendar.classList.add('d-none')
    containerCalendar.classList.remove('d-none')

    data.projects.map(project => createEvent(project, '#28a745'))
    data.programs.map(program => createEvent(program, '#007bff'))
    data.modules.map(module => createEvent(module, '#343a40'))

    renderCalendar(events)
}))

function createEvent(data, color) {
    events.push({
        title: data.name,
        url: data.pk,
        start: data.planning_date,
        color: color // override!
    })
}

function renderCalendar(events) {
    var calendar = new FullCalendar.Calendar(calendarEle, {
        events: events
    });

    calendar.render();
}
