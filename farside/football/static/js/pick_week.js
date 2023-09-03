'use strict';

const team_select = document.querySelectorAll('.team_select');

const clearPoint = (team) => (team.value = -1);

const checkGameSelection = (c) => {
    const location = c.dataset.point === 'away' ? 'home' : 'away';
    const game_teams = c.parentElement.querySelectorAll(':scope > select');
    game_teams.forEach((team) => {
        if (team.dataset.point === location && team.value > 0) {
            // removeListTeam(ct.previousElementSibling.textContent);
            clearPoint(team);
        }
    });
    if (c.value > -1) {
        team_select.forEach((team) => {
            if (c.value === team.value)
                if (c.previousElementSibling.textContent != team.previousElementSibling.textContent) team.value = -1;
        });
    }
};

const checkGameGrid = (c) => {
    const nameReplaced = checkListTeam(c);
    gameTeam.forEach((team) => {
        if (t.textContent === nameReplaced) {
            clearPoint(team.nextElementSibling);
            // removeBGC(team);
        }
    });
};

const SetSaveValues = (choice) => {
    const inputValue = choice.parentElement.querySelector('.u-hidden-input > .input__value');
    const inputWeek = choice.parentElement.querySelector('.u-hidden-input > .input__week');
    const inputGame = choice.parentElement.querySelector('.u-hidden-input > .input__game');
    const inputTeam = choice.parentElement.querySelector('.u-hidden-input > .input__team');

    inputValue.value = choice.value;
    inputWeek.value = 1;
    inputGame.value = choice.parentElement.dataset.game;
    inputTeam.value = choice.dataset.team;
};

const checkGamePick = (choice) => {
    checkGameSelection(choice);
    SetSaveValues(choice);
    // checkGameGrid(choice);
};

const checkPick = (el) => {
    checkGamePick(el);
    // setList(el);
    // setBackground(el);
};

team_select.forEach((team) =>
    team.addEventListener('change', function (e) {
        checkPick(team);
    })
);
