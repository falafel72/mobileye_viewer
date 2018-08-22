document.addEventListener('DOMContentLoaded',function(){
    var lane_ctx = document.getElementById('lane-graph').getContext('2d');
    var speed_ctx = document.getElementById('speed-graph').getContext('2d');
    var heading_ctx = document.getElementById('heading-graph').getContext('2d');
    var time_ctx = document.getElementById('time-graph').getContext('2d');

    var lane_graph = new Chart(lane_ctx, {
        type: 'line',
        data: {
            datasets: [{
                label: 'Left Lane',
                data: [],
                borderColor: '#3E9239'
            }, {
                label: 'Right Lane',
                data: [],
                borderColor: '#374C79'
            }]
        },
        options: {
            scales: {
                xAxes: [{
                    type: 'linear',
                    position: 'bottom'
                }]
            },
            elements: {
                line: {
                    tension: 0
                }
            }
        }
    });

    var speed_graph = new Chart(speed_ctx, {
        type: 'line',
        data: {
            datasets: [{
                label: 'Speed',
                data: [],
                borderColor: '#56357A'
            }]
        },
        options: {
            scales: {
                xAxes: [{
                    type: 'linear',
                    position: 'bottom'
                }]
            },
            elements: {
                line: {
                    tension: 0
                }
            }
        }
    });

    var heading_graph = new Chart(heading_ctx, {
        type: 'line',
        data: {
            datasets: [{
                label: 'Heading',
                data: [],
                borderColor: '#B44B46'
            }]
        },
        options: {
            scales: {
                xAxes: [{
                    type: 'linear',
                    position: 'bottom'
                }]
            },
            elements: {
                line: {
                    tension: 0
                }
            }
        }
    });

    var time_graph = new Chart(time_ctx, {
        type: 'line',
        data: {
            datasets: [{
                label: 'Time',
                data: [],
                borderColor: '#B16B59'
            }]
        },
        options: {
            scales: {
                xAxes: [{
                    type: 'linear',
                    position: 'bottom'
                }]
            },
            elements: {
                line: {
                    tension: 0
                }
            }
        }
    });

    var evtSource = new EventSource('/lanedata');
    evtSource.onmessage = function(evt) {
        var obj = JSON.parse(evt.data);
        addData(lane_graph,0,obj['left']);
        addData(lane_graph,1,obj['right']);
    };
});

function addData(chart,label_idx,data) {
    chart.data.datasets[label_idx].data = data;
    chart.update(0);
}

// function removeData(chart) {
//     chart.data.labels.pop();
//     chart.data.datasets.forEach((dataset) => {
//         dataset.data.pop();
//     });
//     chart.update(0);
// }