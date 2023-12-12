'use strict';

const inputNumbers = document.querySelectorAll('.input__number');

inputNumbers.forEach((number) => {
    number.addEventListener('focus', function (e) {
        if (number.value == 0) {
            number.value = '';
        }
    });
    number.addEventListener('focusout', function (e) {
        if (number.value == '') {
            number.value = 0;
        }
    });
});
