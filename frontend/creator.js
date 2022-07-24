async function fillPage() { printNumbers(); google.setOnLoadCallback(drawCharts); }

async function csvToDict(csvString) {

    var csv_array    = csvString.split(/\n/);
    const dict_keys = csv_array.shift().split(',');

    var csv_dict = {};
    for (var key of dict_keys) {
        csv_dict[key] = [];
    }

    while (csv_array.length) {

        var row_array_strings = csv_array.shift().split(',');
        var row_array = row_array_strings.slice(0, 1).concat(row_array_strings.slice(1).map(Number));
        var row_object = _.zipObject(dict_keys, row_array);
        
        for (var key of dict_keys) {
        csv_dict[key].push(row_object[key]);
        }

    }

    return csv_dict;

}

async function printNumbers() {

    try {

        const dati = await fetch("./story.csv");
        const dati_csv = await dati.text();
        const dati_dict = await csvToDict(dati_csv);

        const last_index = dati_dict.data.length - 1;

        document.getElementById("data").innerHTML = dati_dict.data[last_index];
        document.getElementById("perc").innerHTML = String(dati_dict.perc_story[last_index])+"%";
        document.getElementById("ospedalizzati").innerHTML = dati_dict.ospedalizzati_story[last_index];
        document.getElementById("terapie").innerHTML = dati_dict.terapie_story[last_index];
        document.getElementById("deceduti").innerHTML = dati_dict.deceduti_story[last_index];

        const popolazione_lombarda = 10060965;
        const popolazione_lombarda_over12 = popolazione_lombarda - 1051819;

        const secondadose_perc = String((dati_dict.secondadose_story[dati_dict.secondadose_story.length-1] / popolazione_lombarda * 100).toFixed(2))+"%";
        document.getElementById("secondedosi").style.width = secondadose_perc;
        document.getElementById("secondedosi").innerHTML = secondadose_perc;

        const secondadose_perc_12anni = String((dati_dict.secondadose_story[dati_dict.secondadose_story.length-1] / popolazione_lombarda_over12 * 100).toFixed(2))+"%";
        document.getElementById("secondedosi_12anni").style.width = secondadose_perc_12anni;
        document.getElementById("secondedosi_12anni").innerHTML = secondadose_perc_12anni;

        const terzadose_perc = String((dati_dict.terzadose_story[dati_dict.terzadose_story.length-1] / popolazione_lombarda * 100).toFixed(2))+"%";
        document.getElementById("terzedosi").style.width = terzadose_perc;
        document.getElementById("terzedosi").innerHTML = terzadose_perc;

    } catch(error) {
        console.error(error);
    }

}

async function drawCharts() {

    try {

        const dati = await fetch("./story.csv");
        const dati_csv = await dati.text();
        const dati_dict = await csvToDict(dati_csv);

        curve(  values = [dati_dict['perc_story']],
                colors = ['#fcd2cf', '#f33a30'],
                titles = ["valore assoluto", "media mobile"],
                y_label = "rapporto = pos/tam",
                element_id = "grafico_rapporto",
                with_mean = true,
                startDate = new Date(2020, 8, 1));            // months are 0-indexed
        curve(  [dati_dict['ospedalizzati_story']],
                ['#f99726'],
                ["valore assoluto"],
                "ospedalizzati",
                'grafico_ospedalizzati',
                false,
                new Date(2020, 8, 1));
        curve(  [dati_dict['terapie_story']],
                ['#44a546'],
                ["valore assoluto"],
                "t.i. occupate",
                'grafico_terapie',
                false,
                new Date(2020, 8, 1));
        histo(  dati_dict['deceduti_story'],
                ['#9fcef9', '#1c8af2'],
                ["valore assoluto", "media mobile"],
                "deceduti giornalieri",
                'grafico_deceduti',
                true,
                new Date(2020, 8, 1));
        curve(  [dati_dict['terzadose_story'].slice(123), dati_dict['secondadose_story'].slice(123)],
                ['#e91e62', '#9023a8'],
                ["terze dosi", "seconde dosi"],
                "dosi somministrate",
                'grafico_vaccini',
                false,
                new Date(2021, 0, 2));

    } catch(error) {
        console.error(error);
    }
    
}