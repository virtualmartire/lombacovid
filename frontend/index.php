<!DOCTYPE html>
<html>
<head>

  <!-- Global site tag (gtag.js) - Google Analytics -->
  <script async src="https://www.googletagmanager.com/gtag/js?id=UA-181057130-1"></script>
  <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){dataLayer.push(arguments);}
      gtag('js', new Date());

      gtag('config', 'UA-181057130-1');
  </script>

  <!-- Calendario zone -->
  <script type="text/javascript">
  function ZoneColor(){
    
      		var current_date = new Date().getDate();
      		var yellow = [];
      		var oranges = [];
      		
      		if(current_date > 29){
      			document.getElementById("zona").style.color = "orange";
      			document.getElementById("zona").innerHTML = "arancione";
      		} else {
      		  	document.getElementById("zona").style.background = "#e6e600";
       	 		document.getElementById("zona").style.color = "white";
        		document.getElementById("zona").innerHTML = "gialla";
      		}
      
      		/*
      		if ( yellow.some(item => item == current_date) ){
        		document.getElementById("zona").style.background = "#e6e600";
       	 		document.getElementById("zona").style.color = "white";
        		document.getElementById("zona").innerHTML = "gialla";
      		} else {
      			if ( oranges.some(item => item == current_date) ){
        			document.getElementById("zona").style.color = "orange";
        			document.getElementById("zona").innerHTML = "arancione";
      			} else {
        			document.getElementById("zona").style.color = "red";
        			document.getElementById("zona").innerHTML = "rossa";
        		}
        	}
        	*/
        
  }
  </script>

  <!-- Le icone -->
  <script src="https://kit.fontawesome.com/9c153dbbbb.js" crossorigin="anonymous"></script>

  <title>lombacovid.it</title>

  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">

  <link rel="stylesheet" href="css/w3.css">
  <link rel="stylesheet" href="css/raleway.css">
  <link rel="stylesheet" href="css/font-awesome.css">
  <style>
    html,body,h1,h2,h3,h4,h5 {font-family: "Raleway", sans-serif}
  </style>

</head>

<body onLoad='ZoneColor()'>

<!-- Top bar -->
<div class="w3-bar w3-top w3-black w3-large" style="z-index:4">
  <span class="w3-bar-item w3-right">lombacovid.it</span>
</div>

<!-- !PAGE CONTENT! -->
<div class="w3-main" style="margin-left:150px;margin-right:150px;margin-top:43px;">

  <!-- -->
  <header class="w3-container" style="padding-top:22px">
    <h5>Dati della seconda ondata di <b>coronavirus</b> inerenti alla regione <b>Lombardia (zona <span id="zona">&ensp;&ensp;&ensp;&nbsp;</span>)</b> aggiornati alle 17:00 del <b><?php include("pantarei/data.txt");?></b>.</h5>
  </header>
  <!-- -->

  <!-- -->
  <div class="w3-row-padding w3-margin-bottom">

    <div class="w3-quarter">
      <div class="w3-container w3-red w3-padding-16">
        <div class="w3-left"><i class="fas fa-radiation w3-xxxlarge"></i></div>
        <div class="w3-right">  <h3><?php include("pantarei/perc.txt");?></h3>  </div>
        <div class="w3-clear"></div>
        <h4>Rapporto</h4>
      </div>
    </div>

    <div class="w3-quarter">
      <div class="w3-container w3-orange w3-padding-16">
        <div class="w3-left" style="color:white"><i class="fas fa-ambulance w3-xxxlarge"></i></div>
        <div class="w3-right" style="color:white">  <h3><?php include("pantarei/ospedalizzati.txt");?></h3>  </div>
        <div class="w3-clear"></div>
        <h4 style="color:white">Ospedalizzati</h4>
      </div>
    </div>

    <div class="w3-quarter">
      <div class="w3-container w3-green w3-padding-16">
        <div class="w3-left"><i class="fas fa-procedures w3-xxxlarge"></i></div>
        <div class="w3-right">  <h3><?php include("pantarei/terapie_attuali.txt");?></h3>   </div>
        <div class="w3-clear"></div>
        <h4>T. Intensive</h4>
      </div>
    </div>

    <div class="w3-quarter">
      <div class="w3-container w3-blue w3-text-white w3-padding-16">
        <div class="w3-left"><i class="fas fa-hand-holding-medical w3-xxxlarge"></i></div>
        <div class="w3-right">  <h3><?php include("pantarei/deceduti_oggi.txt");?></h3>  </div>
        <div class="w3-clear"></div>
        <h4>Deceduti</h4>
      </div>
    </div>

  </div>
  <!-- -->

  <!-- -->
  <div class="w3-panel">
    <div class="w3-row-padding" style="margin:0 -16px">
      <div class="w3-half">
        <img src="pantarei/rapporto_graph.png" style="width:100%">
      </div>
      <div class="w3-half">
        <img src="pantarei/ospedalizzati_graph.png" style="width:100%">
      </div>
    </div>
  </div>
  <!-- -->

  <!-- -->
  <div class="w3-panel">
    <div class="w3-row-padding" style="margin:0 -16px">
      <div class="w3-half">
        <img src="pantarei/terapie_attuali_graph.png" style="width:100%">
      </div>
      <div class="w3-half">
        <img src="pantarei/deceduti_giornalieri_graph.png" style="width:100%">
      </div>
    </div>
  </div>
  <!-- -->

  <!-- -->
  <div class="w3-panel">
    <div class="w3-row-padding" style="margin:0 -16px">
      <div class="w3-half">
        <img src="pantarei/vaccini_graph.png" style="width:100%">
      </div>
      <div class="w3-half">
        <h5 style="margin-top:42px; margin-left:15px">Percentuale di persone che hanno ricevuto almeno la prima dose di vaccino:</h5>
        <div class="w3-grey" style="margin-left:15px;margin-right:15px">
        <div class="w3-container w3-center w3-padding w3-purple" style="width:<?php include("pantarei/primadose_perc.txt");?>"><?php include("pantarei/primadose_perc.txt");?></div>
        </div>
        <h5 style="margin-top:42px; margin-left:15px">Percentuale di persone vaccinate completamente:</h5>
        <div class="w3-grey" style="margin-left:15px;margin-right:15px">
        <div class="w3-container w3-center w3-padding w3-purple" style="width:<?php include("pantarei/secondadose_perc.txt");?>"><?php include("pantarei/secondadose_perc.txt");?></div>
        </div>
      </div>
    </div>
  </div>
  <!-- -->

  <hr />

  <div class="w3-container">
    <h5>Il testo ufficiale dell'ultimo DPCM generale lo trovi <a href="https://www.gazzettaufficiale.it/eli/id/2021/01/15/21A00221/sg" target="_blank">qui</a>.
  </div>
  <div class="w3-container" style="padding-bottom:22px">
    <h5>Se vuoi sapere perch&eacute ho scelto di analizzare proprio questi dati <a href="spiegazione.html">clicka qui</a>. Se invece vuoi sapere chi sono io <a href="https://www.stefanomartire.it" target="_blank">clicka qui</a>.</h5>
  </div>

</div>
<!-- End page content -->

<!-- Footer -->
  <footer class="w3-container w3-padding-16 w3-light-grey">
    <p class="w3-right">Styled with <a href="https://www.w3schools.com/w3css/default.asp" target="_blank">w3.css</a>.</p>
  </footer>

</body>
</html>