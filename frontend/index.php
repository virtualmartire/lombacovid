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

	<title>LombaCovid</title>
	<meta name="viewport" content="width=device-width, initial-scale=1.0">
	<link rel="stylesheet" href="vestiti.css">
</head>
<body>

	<p>
		<div class="muro">
			Dati della seconda ondata di <b>coronavirus</b> inerenti alla regione <b>Lombardia (zona <span style="color:orange">arancione</span>)</b> aggiornati alle 17:00 del <b><?php include("pantarei/data.txt");?></b>.
		</div>
		<div class="muro">
			Se vuoi sapere perch&eacute ho scelto di analizzare proprio questi <a href="spiegazione.html">clicka qui</a>. Se vuoi sapere chi sono io <a href="sm.html">clicka qui</a>.
		</div>
	</p>

	<p class="muro">
		Data di entrata in vigore dell'<a href="https://www.gazzettaufficiale.it/eli/id/2020/11/04/20A06109/sg" target="_blank">ultimo DPCM</a>: 6/11/2020. Data di inizio della sua efficacia: 20/11/2020.
	</p>

	<p>
		<div class="label">RAPPORTO: <?php include("pantarei/perc.txt");?></div>
		<br />
		<div class="labelino">POSITIVI ACCERTATI OGGI: <?php include("pantarei/nuovipos.txt");?></div>
		<div class="labelino">TAMPONI OGGI: <?php include("pantarei/tam.txt");?></div>
		<img src="pantarei/rapporto_graph.png" class="centered_img">
		<br />
	</p>
	<p>
		<div class="label">OSPEDALIZZATI ATTUALI: <?php include("pantarei/ospedalizzati.txt");?></div>
		<img src="pantarei/ospedalizzati_graph.png" class="centered_img">
		<br /><br />
		<div class="label">TERAP. INT. ATTUALI: <?php include("pantarei/terapie_attuali.txt");?></div>
		<img src="pantarei/terapie_attuali_graph.png" class="centered_img">
		<br /><br />
		<div class="label">DECEDUTI OGGI: <?php include("pantarei/deceduti_oggi.txt");?></div>
		<img src="pantarei/deceduti_giornalieri_graph.png" class="centered_img">
	</p>
	
</body>
</html>