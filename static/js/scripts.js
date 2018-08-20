document.addEventListener('DOMContentLoaded',function(){
    // alert("HI")
    var evtSource = new EventSource('/lanedata');
    evtSource.onmessage = function(evt) {
        console.log(evt.data);
    };

});
