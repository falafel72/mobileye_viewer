document.addEventListener('DOMContentLoaded',function(){
    var lane_ctx = document.getElementById('lane-graph').getContext('2d');
    var speed_ctx = document.getElementById('speed-graph').getContext('2d');
    var heading_ctx = document.getElementById('heading-graph').getContext('2d');
    var time_ctx = document.getElementById('time-graph').getContext('2d');

    var lane_graph = new Chart(lane_ctx, {
        type: 'scatter',
        data: {
            datasets: [{
                label: 'Left Lane',
                data: []
            }, {
                label: 'Right Lane',
                data: []
            }]
        },
        options: {
            scales: {
                xAxes: [{
                    type: 'linear',
                    position: 'bottom'
                }]
            }
        }
    });

    var speed_graph = new Chart(speed_ctx, {
        type: 'scatter',
        data: {
            datasets: [{
                label: 'Speed',
                data: []
            }]
        },
        options: {
            scales: {
                xAxes: [{
                    type: 'linear',
                    position: 'bottom'
                }]
            }
        }
    });

    var heading_graph = new Chart(heading_ctx, {
        type: 'scatter',
        data: {
            datasets: [{
                label: 'Speed',
                data: []
            }]
        },
        options: {
            scales: {
                xAxes: [{
                    type: 'linear',
                    position: 'bottom'
                }]
            }
        }
    });

    var time_ctx = new Chart(time_ctx, {
        type: 'scatter',
        data: {
            datasets: [{
                label: 'Speed',
                data: []
            }]
        },
        options: {
            scales: {
                xAxes: [{
                    type: 'linear',
                    position: 'bottom'
                }]
            }
        }
    });

    var evtSource = new EventSource('/lanedata');
    evtSource.onmessage = function(evt) {
        console.log(evt.data);
    };
});

function addData(chart,label,data) {
    chart.data.labels.push(label);
    chart.data.datasets.forEach((dataset) => {
        dataset.data.push(data);
    });
    chart.update();
}

function removeData(chart) {
    chart.data.labels.pop();
    chart.data.datasets.forEach((dataset) => {
        dataset.data.pop();
    });
    chart.update();
}