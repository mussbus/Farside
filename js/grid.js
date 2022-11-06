'use strict';

const selectPick = document.querySelectorAll('.selection__game-choice');
const gameTeam = document.querySelectorAll('.selection__game-team');
const listPoint = document.querySelectorAll('.selection__list-point');
const listTeam = document.querySelectorAll('.selection__list-team');

const GAMES_IN_WEEK = 16;

const addTeam = function (name, pointValue) {
  pointValue += '';
  listPoint.forEach(function (p) {
    if (p.textContent.slice(0, -1) === pointValue)
      p.nextElementSibling.textContent = name;
  });
};
const removeTeam = function (name) {
  listTeam.forEach(function (t) {
    if (t.textContent === name) t.textContent = '';
  });
};

const checkListTeam = c => {
  const pointValue = c.selectedIndex + '';
  let returnName = null;
  listPoint.forEach(function (p) {
    if (p.textContent.slice(0, -1) === pointValue) {
      returnName = p.nextElementSibling.textContent;
    }
  });
  return returnName;
};

const clearPoint = c => (c.selectedIndex = 0);
const checkGameGrid = c => {
  const nameReplaced = checkListTeam(c);
  gameTeam.forEach(t => {
    if (t.textContent === nameReplaced) {
      clearPoint(t.nextElementSibling);
      removeBGC(t);
    }
  });
};
const checkGameSelection = c => {
  const location = c.dataset.point === 'away' ? 'home' : 'away';
  const childTeam = c.parentElement.querySelectorAll(':scope > select');
  childTeam.forEach(ct => {
    if (ct.dataset.point === location && ct.selectedIndex > 0) {
      removeTeam(ct.previousElementSibling.textContent);
      clearPoint(ct);
    }
  });
};

const addBGC = c => c.parentElement.classList.add('u-bgc-green');
const removeBGC = c => c.parentElement.classList.remove('u-bgc-green');

const setBackground = function (choice) {
  choice.selectedIndex > 0 ? addBGC(choice) : removeBGC(choice);
};
const setList = function (choice) {
  const teamName = choice.previousElementSibling.textContent;
  removeTeam(teamName);
  addTeam(teamName, choice.selectedIndex);
};
const checkGamePick = function (choice) {
  checkGameSelection(choice);
  checkGameGrid(choice);
};

selectPick.forEach(c =>
  c.addEventListener('change', function (e) {
    checkGamePick(c);
    setList(c);
    setBackground(c);
  })
);

const populateSelect = function () {
  let markup = '';
  for (let i = 0; i <= GAMES_IN_WEEK; i++)
    markup += `<option value="${i}">${i}</option>`;
  return markup;
};

const init = function () {
  selectPick.forEach(c => (c.innerHTML = populateSelect()));
};

init();
