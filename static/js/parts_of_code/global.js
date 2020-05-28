
const utilUril = new UtilUrl()

const tabMenu1 = document.getElementById('tab1')
const tabMenu2 = document.getElementById('tab2')
const tabMenu3 = document.getElementById('tab3')


let paramUrl = utilUril.getParameterByName('type_part')


switch (paramUrl) {
    case 'reused':
        tabMenu2.checked = true
        break;

    case 'new':
        tabMenu3.checked = true
        break;

    default:
        tabMenu1.checked = true;
}


tabMenu1.addEventListener('click', (e) => utilUril.changeUrlParam('type_part', 'base'))
tabMenu2.addEventListener('click', (e) => utilUril.changeUrlParam('type_part', 'reused'))
tabMenu3.addEventListener('click', (e) => utilUril.changeUrlParam('type_part', 'new'))




