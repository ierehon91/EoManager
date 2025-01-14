async function get_tickets_list() {
    let update_button = document.getElementById('update-ticket-list-button')
    update_button.innerHTML = 'Идёт обновление...';


    let formData = new URLSearchParams({
        'date': document.querySelector('input[name="date"]').value,
        'division': document.querySelector('select[name="division"]').value,

        'prerecord': document.querySelector('input[name="prerecord"]').checked,
        'notprerecord': document.querySelector('input[name="notprerecord"]').checked,
    })

    let statuses = document.getElementsByClassName('statuses-form')
    for (let i=0; i < statuses.length; i++) {
        formData.append(statuses[i].name, statuses[i].checked)
    }

    let encoding_url = `${load_tickets_list_url}?${formData.toString()}`;

    let options = {
        method: 'get',
        mode: 'same-origin',
    }


    let response = await fetch(encoding_url, options)
    let text = await response.text()
    let json = await JSON.parse(text)
    await render_table(json.content);

    update_button.innerHTML = 'Обновить';
}


async function render_table(data) {
    $('.ticket-list-body').html('')

    for (let i = 0; i < data.length; i++) {
        queueDate = `<td>${data[i]['queueDate']}</td>`
        ticketcode = `<td class="ticketcode">${data[i]['ticketcode']}</td>`
        state = create_state_row(data[i]['recordstate'], data[i]['employee'])
        waitTime = `<td class="waitTimeStatus waitTimeStatus-${data[i]['waitTime']['status']}"><span>${data[i]['waitTime']['wait']}</span></td>`
        type_ticket = `<td>${encode_type_record(data[i]['isprerecord'])}</td>`
        service = `<td>${data[i]['servicegroup']['name']}</td>`
        consumer = create_consumer_row(data[i]['fio'], data[i]['phone'])
        specialist = create_specialist_row(data[i]['employee'])
        $('.ticket-list-body').append(`
            <tr style="background-color: ${data[i]['recordstate']['frontend_color']}">
                ${queueDate}
                ${ticketcode}
                ${state}
                ${waitTime}
                ${type_ticket}
                ${service}
                ${consumer}
                ${specialist}
            </tr>
            `)
    }
}

function encode_type_record(isprerecord) {
    if (isprerecord) {
        return 'Предварительная'
    }
    return 'Текущая'
}

function create_state_row(recordstate) {
    result = `<td class="state">
                <div class="state-container">
                    <div class="state-left-side ${recordstate['db_name']}" style="background-color: ${recordstate['frontend_color']}"></div>
                    <div class="state-right-side">${recordstate['frontend_name']}</div>
                </div>
            </td>
            `
    return result
}

function create_consumer_row(fio, phone=null) {
    result = `<td>${fio}`
    if(phone) {
        result += `<br>${phone}`
    }
    result += '</td>'
    return result
}

function create_specialist_row (employee) {
    result = `<td>`
    if (employee) {
        result += `${employee['lastname']} ${employee['firstname']} ${employee['middlename']}`
        if (employee['operatorwindow']) {
            result += `<br>Окно ${employee['operatorwindow']['name']}`
        }
    }
    result += `</td>`
    return result
}
