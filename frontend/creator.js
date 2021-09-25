async function fillPage() { printNumbers(); google.setOnLoadCallback(drawCharts); }

async function printNumbers() {

    try {

        const zone = document.getElementById("zona");
        zone.style.background = "black";
        zone.style.color = "white";
        zone.innerHTML = "bianca";

        const dati = await fetch("./story.json"); const dati_json = await dati.json();

        document.getElementById("data").innerHTML = dati_json.data;
        document.getElementById("perc").innerHTML = String(dati_json.perc_story[dati_json.perc_story.length-1])+"%";
        document.getElementById("ospedalizzati").innerHTML = dati_json.ospedalizzati_story[dati_json.ospedalizzati_story.length-1];
        document.getElementById("terapie").innerHTML = dati_json.terapie_story[dati_json.terapie_story.length-1];
        document.getElementById("deceduti").innerHTML = dati_json.deceduti_story[dati_json.deceduti_story.length-1];

        const popolazione_lombarda = 10060965;
        const popolazione_lombarda_over12 = popolazione_lombarda - 1051819;

        const primadose_perc = String((dati_json.primadose_story[dati_json.primadose_story.length-1] / popolazione_lombarda * 100).toFixed(2))+"%";
        document.getElementById("primedosi").style.width = primadose_perc;
        document.getElementById("primedosi").innerHTML = primadose_perc;

        const secondadose_perc = String((dati_json.secondadose_story[dati_json.secondadose_story.length-1] / popolazione_lombarda * 100).toFixed(2))+"%";
        document.getElementById("secondedosi").style.width = secondadose_perc;
        document.getElementById("secondedosi").innerHTML = secondadose_perc;

        const secondadose_perc_12anni = String((dati_json.secondadose_story[dati_json.secondadose_story.length-1] / popolazione_lombarda_over12 * 100).toFixed(2))+"%";
        document.getElementById("secondedosi_12anni").style.width = secondadose_perc_12anni;
        document.getElementById("secondedosi_12anni").innerHTML = secondadose_perc_12anni;

    } catch(error) {
        console.error(error);
    }

}

async function drawCharts() {

    try {

        const time_series = await fetch('./story.json'); const time_series_json = await time_series.json();

        curve(  values = [time_series_json['perc_story']],
                colors = ['#fcd2cf', '#f33a30'],
                titles = ["valore assoluto", "media mobile"],
                y_label = "rapporto = pos/tam",
                element_id = "grafico_rapporto",
                with_mean = true,
                startDate = new Date(2020, 8, 1));            // months are 0-indexed
        curve(  [time_series_json['ospedalizzati_story']],
                ['#f99726'],
                ["valore assoluto"],
                "ospedalizzati",
                'grafico_ospedalizzati',
                false,
                new Date(2020, 8, 1));
        curve(  [time_series_json['terapie_story']],
                ['#44a546'],
                ["valore assoluto"],
                "t.i. occupate",
                'grafico_terapie',
                false,
                new Date(2020, 8, 1));
        histo(  time_series_json['deceduti_story'],
                ['#9fcef9', '#1c8af2'],
                ["valore assoluto", "media mobile"],
                "deceduti giornalieri",
                'grafico_deceduti',
                true,
                new Date(2020, 8, 1));
        curve(  [time_series_json['primadose_story'], time_series_json['secondadose_story']],
                ['#9023a8', '#9023a8'],
                ["prime dosi", "seconde dosi"],
                "dosi somministrate",
                'grafico_vaccini',
                false,
                new Date(2021, 0, 2));

    } catch(error) {
        console.error(error);
    }
    
}