'use static';

class Point {
    constructor(x, y) {
        this.x = x;
        this.y = y;
    }
}

class DataList {
    constructor(data) {
        this.data = data.list_season_rank.map((d) => new Point(d.x, d.y));
        this.numWeeks = data.list_season_rank.length;
        this.numUsers = data.num_users;
        console.log(data);
    }
}

function createChart(data) {
    const canvas = document.getElementById('season__rank').getContext('2d');
    const dataClass = new DataList(data);
    console.log(dataClass);

    chart = new Chart(canvas, {
        type: 'line',
        data: {
            datasets: [
                {
                    label: 'Chad Season Rank',
                    data: dataClass.data,
                    backgroundColor: ['yellow', 'aqua', 'pink', 'lightgreen', 'gold', 'lightblue'],
                    borderColor: ['black'],
                },
            ],
        },
        options: {
            plugins: {
                title: {
                    // align: 'start',
                    display: true,
                    text: 'Seasonal Rank',
                },
            },
            pointHoverBorderColor: 'green',
            pointRadius: 6,
            pointHoverRadius: 9,
            responsive: true,
            scales: {
                x: {
                    type: 'linear',
                    position: 'bottom',
                    title: {
                        display: true,
                        text: 'Week',
                    },
                    min: 0,
                    max: dataClass.numWeeks + 1,
                    ticks: {
                        // forces step size to be 50 units
                        stepSize: 1,
                    },
                },
                y: {
                    title: {
                        display: true,
                        text: 'Rank',
                    },
                    min: 0,
                    max: dataClass.numUsers,
                },
            },
        },
    });
}
