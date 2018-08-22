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
                data: [],
                backgroundColor: '#3E9239'
            }, {
                label: 'Right Lane',
                data: [],
                backgroundColor: '#374C79'
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
                data: [],
                backgroundColor: '#56357A'
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
                label: 'Heading',
                data: [],
                backgroundColor: '#B44B46'
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

    var time_graph = new Chart(time_ctx, {
        type: 'scatter',
        data: {
            datasets: [{
                label: 'Time',
                data: [],
                backgroundColor: '#B16B59'
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
        // console.log(speed_graph.data.datasets)
        var obj = JSON.parse(evt.data)
        
        addData(speed_graph,0,obj['points']) 
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