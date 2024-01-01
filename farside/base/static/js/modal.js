'use strict';

const modalError = document.getElementById('modal__error');
const modalForm = document.getElementById('modal__form');
const modalDelete = document.getElementById('modal__delete');
const modalContent = document.querySelector('.modal__content');

// if (modalForm != null) {
//     console.log(modalForm);

//     // Get the <span> element that closes the modal
//     const close = modalForm.querySelector('.modal__close');

//     // // When the user clicks on the button, open the modal
//     // btn.onclick = function () {
//     //     modal.style.display = 'block';
//     // };

//     // When the user clicks on <span> (x), close the modal
//     close.onclick = function () {
//         modalForm.classList.add('modal__hidden');
//     };

//     // When the user clicks anywhere outside of the modal, close it
//     window.onclick = function (event) {
//         if (event.target == modalForm) {
//             modalForm.classList.add('modal__hidden');
//         }
//     };
// }

const modalInit = function (modal) {
    if (modal != null) {
        // Get the <span> element that closes the modal
        const close = modal.querySelector('.modal__close');

        // // When the user clicks on the button, open the modal
        // btn.onclick = function () {
        //     modal.style.display = 'block';
        // };

        // When the user clicks on <span> (x), close the modal
        close.onclick = function () {
            modal.classList.add('modal__hidden');
        };

        // When the user clicks anywhere outside of the modal, close it
    }
};

window.onclick = function (event) {
    if (event.target == modalForm) {
        modalForm.classList.add('modal__hidden');
    } else if (event.target == modalError) {
        modalError.classList.add('modal__hidden');
    } else if (event.target == modalDelete) {
        modalDelete.classList.add('modal__hidden');
    }
};

modalInit(modalDelete);
modalInit(modalError);
modalInit(modalForm);
