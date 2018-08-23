document.addEventListener('DOMContentLoaded',function(){
    var lane_ctx = document.getElementById('lane-graph').getContext('2d');
    var speed_ctx = document.getElementById('speed-graph').getContext('2d');
    var heading_ctx = document.getElementById('heading-graph').getContext('2d');

    var lane_graph = new Chart(lane_ctx, {
        type: 'line',
        data: {
            datasets: [{
                label: 'Left Lane',
                data: [],
                borderColor: '#3E9239',
                backgroundColor: 'rgba(0,0,0,0)'
            }, {
                label: 'Right Lane',
                data: [],
                borderColor: '#374C79',
                backgroundColor: 'rgba(0,0,0,0)'
            }]
        },
        options: {
            scales: {
                xAxes: [{
                    type: 'linear',
                    position: 'bottom',
                    ticks: {
                        min: -10,
                        max: 10
                    },
                    scaleLabel: {
                        display: true, 
                        labelString: 'Lateral Distance (m)'
                    }
                }],
                yAxes: [{
                    ticks: {
                        min:-120,
                        max: 120
                    },
                    scaleLabel: {
                        display: true,
                        labelString: 'Forward Distance (m)'
                    }
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
        type: 'horizontalBar',
        data: {
            labels: ['Speed'],
            datasets: [{
                label: 'Speed',
                data: [],
                borderWidth: 0,
                backgroundColor: '#56357A'
            }]
        },
        options: {
            scales: {
                xAxes: [{
                    ticks: {
                        min: 0,
                        max: 120,
                        stepSize: 20
                    }
                }],
                yAxes: [{
                    barPercentage: 0.3
                }]
            }
        }
    });

    var heading_graph = new Chart(heading_ctx, {
        type: 'horizontalBar',
        data: {
            labels: ['Heading'],
            datasets: [{
                label: 'Heading',
                data: [],
                backgroundColor: '#B44B46'
            }]
        },
        options: {
            scales: {
                xAxes: [{
                    ticks: {
                        min: -45,
                        max: 45,
                        stepSize: 5
                    }
                }],
                yAxes: [{
                    barPercentage: 0.3
                }]
            },
        }
    });

    var evtSource = new EventSource('/lanedata');
    evtSource.onmessage = function(evt) {
        var obj = JSON.parse(evt.data);
        addData(lane_graph,0,obj['left']);
        addData(lane_graph,1,obj['right']);
        addData(speed_graph,0,obj['speed']);
        addData(heading_graph,0,obj['heading']);
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