

class ServiceChronometer {

    async updateTime(time, idTimeLog, isPaused){
        const url = `http://localhost:8000/timelogs/${idTimeLog}/pause/?current_time=${time}&is_paused=${isPaused}`

        const response = await fetch(url, {'credentials': 'include'})
        const data = await response.json()

        return data
    }

}