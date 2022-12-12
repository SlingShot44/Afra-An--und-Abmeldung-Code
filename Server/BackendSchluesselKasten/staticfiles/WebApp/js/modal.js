let modal = document.querySelector('.modal');
let form = modal.querySelector('form');
let subFunc = (e) => {
    e.preventDefault();
    let formData = new FormData(form);
    fetch(form.action, {
        method: form.method,
        body: formData,
    }).then(response =>
        response.text()
    ).then(data => {
        document.querySelector('.modal-body').innerHTML = data;
        $('.django-select2').djangoSelect2({ placeholder: 'Schüler auswählen' });
    })
    return false;
}