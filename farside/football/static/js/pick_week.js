'use strict';

const team_list = document.querySelectorAll('.input__select');
const listDisplay = document.querySelectorAll('.pick__list-item');

const gameCount = listDisplay.length;

const clearPoint = (team) => (team.value = -1);

const checkGameSelection = (team) => {
    const location = team.dataset.location === 'away' ? 'home' : 'away';
    const game_teams = team.parentElement.querySelectorAll(':scope > select');

    game_teams.forEach((team) => {
        if (team.dataset.location === location && team.value > 0) {
            // removeListTeam(ct.previousElementSibling.textContent);
            console.log(true);
            clearPoint(team);
        }
    });

    if (team.value > -1) {
        team_list.forEach((teams) => {
            if (team.value === teams.value)
                if (team.previousElementSibling.textContent != teams.previousElementSibling.textContent) {
                    teams.value = -1;
                    setBackground(teams);
                }
        });
    }
};

const setBackground = (team) => {
    let valid = true;
    const game = team.parentElement;
    const game_teams = game.querySelectorAll(':scope > select');

    if (game_teams[0].value > 0 && game_teams[1].value > 0) valid = false;
    else if (game_teams[0].value < 0 && game_teams[1].value < 0) valid = false;

    if (valid) {
        game.classList.add('pick__game-valid');
        game_teams.forEach((team) => {
            team.classList.remove('input__error');
        });
    } else game.classList.remove('pick__game-valid');
};

const checkGameGrid = (team) => {
    const nameReplaced = checkListTeam(team);
    gameTeam.forEach((team) => {
        if (t.textContent === nameReplaced) {
            clearPoint(team.nextElementSibling);
            // removeBGC(team);
        }
    });
};

const checkGamePick = (team) => {
    checkGameSelection(team);
    // checkGameGrid(choice);
};

function setList(team) {
    listDisplay.forEach((item) => {
        const spans = item.getElementsByTagName('span');
        if (spans[1].innerText === team.previousElementSibling.innerText) {
            spans[1].innerText = '';
        }
    });

    const replaceTeamText = listDisplay[gameCount - team.value].getElementsByTagName('span');
    replaceTeamText[1].innerText = team.previousElementSibling.innerText;
}

const init = () => {
    team_list.forEach((team) => {
        setBackground(team);
        team.addEventListener('change', function (e) {
            checkGamePick(team);
            setBackground(team);
            setList(team);
        });
    });
};

init();
