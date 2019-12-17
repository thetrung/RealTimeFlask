$(document).ready(function(){

    //connect to the socket server.
    var socket = io.connect('http://' + document.domain + ':' + location.port + '/test');
    var numbers_received = [];
    var numbers_labels = [];

    // Global parameters:
    // do not resize the chart canvas when its container does (keep at 600x400px)
    Chart.defaults.global.responsive = true;

    // get chart canvas
    var ctx = document.getElementById("myChart").getContext("2d");

    // define the chart data
    var chartData = {
    labels : numbers_received,
    datasets : [{
        label: "data",
        fill: true,
        lineTension: 0.1,
        backgroundColor: "rgba(75,192,192,0.4)",
        borderColor: "rgba(75,192,192,1)",
        borderCapStyle: 'butt',
        borderDash: [],
        borderDashOffset: 0.0,
        borderJoinStyle: 'miter',
        pointBorderColor: "rgba(75,192,192,1)",
        pointBackgroundColor: "#fff",
        pointBorderWidth: 1,
        pointHoverRadius: 5,
        pointHoverBackgroundColor: "rgba(75,192,192,1)",
        pointHoverBorderColor: "rgba(220,220,220,1)",
        pointHoverBorderWidth: 2,
        pointRadius: 1,
        pointHitRadius: 10,
        data : numbers_received,
        spanGaps: false
    }]
    }

    // create the chart using the chart canvas
    var lineChart = new Chart(ctx, {
      type: 'line',
      data: chartData,
    });
    // Avoid re-animate the chart on updating data.
    lineChart.options.duration = 0;

    //receive details from server
    socket.on('newnumber', function(msg) {
        // Log
        console.log("Received number :" + msg.number + " -- label :" + msg.label);

        //maintain a list of ten numbers
        if (numbers_received.length >= 50){
            numbers_labels.shift();
            numbers_received.shift();
        }
        numbers_labels.push(msg.label);
        numbers_received.push(msg.number);

        lineChart.data.labels = numbers_labels;
        lineChart.data.datasets.data = numbers_received;

        lineChart.update();
    });
});
