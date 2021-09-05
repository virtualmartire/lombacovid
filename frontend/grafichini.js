google.charts.load('current', {'packages':['corechart'], 'language': 'it'});

Date.prototype.addDay = function(days) {
    var date = new Date(this.valueOf());
    date.setDate(date.getDate() + days);
    return date;
}
  
function getDatesArray(startDate, stopDate) {
    var datesArray = new Array();
    var currentDate = startDate;
    while (currentDate <= stopDate) {
          
        // Adding the date to array
        datesArray.push(new Date(currentDate)); 
          
        // Increment the date by 1 day
        currentDate = currentDate.addDay(1); 

    }
    return datesArray;
}

function zip_arrays(array_of_arrays) {

    if (array_of_arrays.length == 2) {
        return array_of_arrays[0].map( (e,i) => [e, array_of_arrays[1][i]] );
    } else {
        return array_of_arrays[0].map( (e,i) => [e, array_of_arrays[1][i], array_of_arrays[2][i]] );
    }

}

/////////////////////////////////////////////////////////////////////////////////

/* Curva  */
function curve(values, colors, titles, y_label, element_id, with_mean = false, startDate) {

    const y_1 = values[0];

    const stopDate = startDate.addDay(y_1.length);
    const x = getDatesArray(startDate, stopDate);

    var datatable = [];
    if (with_mean == true || values.length == 2) {
        
        var y_2 = [];
        if (with_mean == true) {
            y_1.forEach((element, i) => {
                if ( i > 1 && i < (y_1.length -2) ) {
                    y_2.push((y_1[i-2] + y_1[i-1] + y_1[i] + y_1[i+1] + y_1[i+2]) / 5);
                } else {
                    y_2.push(element);
                }
            });
        } else {
            y_2 = values[1];
        }

        datatable = zip_arrays([x, y_1, y_2]);

    } else {
        datatable = zip_arrays([x, y_1]);
    }

    var data = new google.visualization.DataTable();
    data.addColumn('date', "giorno");
    data.addColumn('number', titles[0]);
    if (with_mean == true || values.length == 2) {
        data.addColumn('number', titles[1]);
    }

    data.addRows(datatable);

    var options = {
        series: {
            0: { color: colors[0] }
        },
        legend: {position: 'none'},
        height: 500,
        hAxis: { textStyle: {fontSize: 14} },
        vAxis: { textStyle: {fontSize: 14} },
        chartArea: {width: '70%', height: '70%'}
    };
    if (values.length != 2) {
        options.vAxis.title = y_label;
    }
    if (with_mean == true || values.length == 2) {
        options.series[0].lineDashStyle = [3, 3];
        options.series[1] = { color: colors[1], lineDashStyle: [3, 0] };
        options.legend.position = 'top';
    }

    var chart = new google.visualization.LineChart( document.getElementById(element_id) );

    chart.draw(data, options);

}

/* Istogramma */
function histo(values, colors, titles, y_label, element_id, with_mean = false, startDate) {

    const y = values;

    const stopDate = startDate.addDay(y.length);
    const x = getDatesArray(startDate, stopDate);

    var datatable = [];
    if (with_mean == true) {

        var y_fit = [];
        y.forEach((element, i) => {
            if ( i > 1 && i < (y.length -2) ) {
                y_fit.push((y[i-2] + y[i-1] + y[i] + y[i+1] + y[i+2]) / 5);
            } else {
                y_fit.push(element);
            }
        });
        datatable = zip_arrays([x, y, y_fit]);

    } else {
        datatable = zip_arrays([x, y]);
    }

    var data = new google.visualization.DataTable();
    data.addColumn('date', "giorno");
    data.addColumn('number', titles[0]);
    if (with_mean == true) {
        data.addColumn('number', titles[1]);
    }

    data.addRows(datatable);

    var options = {
        series: {
            0: { color: colors[0], type: 'bars' }
        },
        legend: {position: 'none'},
        height: 500,
        hAxis: { textStyle: {fontSize: 14} },
        vAxis: { title: y_label, textStyle: {fontSize: 14} },
        chartArea: {width: '70%', height: '70%'}
    };
    if (with_mean == true) {
        options.series[1] = { color: colors[1], type: 'line' };
        options.legend.position = 'top';
    }

    var chart = new google.visualization.ComboChart( document.getElementById(element_id) );

    chart.draw(data, options);

}