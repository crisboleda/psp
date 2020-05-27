
const alertsNotification = document.getElementsByClassName('alertNotification')


class AlertManager {

    static hidden(alert){
        setTimeout(() => {
            alert.classList.add('hidden-animation-alert')
            setTimeout(() => {
                alert.classList.add('d-none')
            }, 700)
        }, 4500)
    }
}


if (alertsNotification){
    for (let i = 0; i < alertsNotification.length; i++) {
        AlertManager.hidden(alertsNotification[i])
    }
}
