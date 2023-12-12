'use strict';

const formsetContainer = document.getElementById('formset_container');
const add = document.getElementById('btn_add');
const remove = document.getElementById('btn_remove');
const minNumForms = document.getElementById('id_form-MIN_NUM_FORMS');
const maxNumForms = document.getElementById('id_form-MAX_NUM_FORMS');
const totalForms = document.getElementById('id_form-TOTAL_FORMS');

add.addEventListener('click', addForm);
remove.addEventListener('click', removeForm);

function addForm(e) {
    e.preventDefault();
    let gameForms = document.querySelectorAll('.form__form');

    if (gameForms.length == maxNumForms.value) return;

    let newForm = gameForms[gameForms.length - 1].cloneNode(true);
    newForm.innerHTML = newForm.innerHTML.replace(`${gameForms.length}`, `${gameForms.length + 1}`);
    newForm.innerHTML = newForm.innerHTML.replaceAll(`${gameForms.length - 1}`, `${gameForms.length}`);

    formsetContainer.insertAdjacentElement('beforeend', newForm);
    if (gameForms.length + 1 == maxNumForms.value) add.disabled = true;
    remove.disabled = false;
}

function removeForm(e) {
    e.preventDefault();
    let gameForms = document.querySelectorAll('.form__form');
    console.log(gameForms.length);
    console.log(minNumForms.value);

    if (gameForms.length == minNumForms.value) return;

    console.log('enabled');

    const lastForm = gameForms[gameForms.length - 1];
    lastForm.remove();
    totalForms.value = gameForms.length - 1;

    if (gameForms.length - 1 == minNumForms.value) remove.disabled = true;
    add.disabled = false;
    console.log('remove');
}

function init() {
    let gameForms = document.querySelectorAll('.form__form');
    if (gameForms.length == maxNumForms.value) add.disabled = true;
    else if (gameForms.length == minNumForms.value) remove.disabled = true;
}

init();
