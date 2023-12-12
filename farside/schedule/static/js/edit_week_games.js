'use strict';

const delete_list = document.querySelectorAll('.delete');
const edit_list = document.querySelectorAll('.edit');
const add_button = document.querySelector('.button__add');
const modal_header = document.querySelector('.heading__tertiary');
const game_id = document.getElementById('id_game_id');

const away_team = document.getElementById('id_away_team');
const home_team = document.getElementById('id_home_team');

// edit_list.forEach((edit) => {
//     edit.addEventListener('click', function (e) {
//         modal.classList.remove('modal__hidden');
//         away_team.value = edit.parentElement.nextElementSibling.dataset.id;
//         home_team.value = edit.parentElement.nextElementSibling.nextElementSibling.dataset.id;
//         modal_header.textContent = 'Edit Game';
//         game_id.value = +edit.dataset.game;
//     });
// });

const init = function () {
    // modalContent.classList.add('modal__small');
};

init();

document.onclick = function (event) {
    // Compensate for IE<9's non-standard event model
    //
    if (event === undefined) event = window.event;
    var target = 'target' in event ? event.target : event.srcElement;

    console.log('clicked on ' + target.tagName);
};
