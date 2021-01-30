from matplotlib import pyplot as plt
import matplotlib.ticker as mticker
from datetime import date, timedelta

def curve(path, filename, color, ylabel):

	f = open(path)
	y = []
	x = []
	k = -1
	for line in f:
		if k != -1:		#perché la prima riga dei file "story" è vuota
			y.append( float(line) )
			x.append(k)
		k = k+1
	f.close()

	#faccio in modo che le etichette sull'asse x non siano più di 7
	f = open("timestep.txt")
	for line in f:
		timestep = int(line)
	f.close()
	if len( range(0, k, timestep) ) > 7:
		f = open("timestep.txt", 'w')
		timestep = timestep + 1
		f.write( str(timestep) )
		f.close()

	#preparo l'array delle date
	a = date(2020, 9, 1)
	b = date.today()
	gap = b - a
	gap = int(gap.days)
	date_list = []
	for z in range(0, gap+1, timestep):	#gap+1 non incluso in range(0, gap+1)
		p = a + timedelta(days=z)
		p = p.strftime("%d/%m")
		date_list.append(p)

	plt.plot(x, y, color=color)
	plt.xticks( range(0, k, timestep), date_list )
	plt.xlabel("data", fontsize = 14)
	plt.ylabel(ylabel, fontsize=14)
	plt.grid(linewidth=0.5)
	plt.savefig("pantarei/" + filename + "_graph.png", dpi=300)
	plt.clf()

def histo(path, filename, color, ylabel):

	f = open(path)
	y = []
	x = []
	k = -1
	for line in f:
		if k != -1:
			y.append( float(line) )
			x.append(k)
		k = k+1
	f.close()

	f = open("timestep.txt")
	for line in f:
		timestep = int(line)
	f.close()
	if len( range(0, k, timestep) ) > 7:
		f = open("timestep.txt", 'w')
		timestep = timestep + 1
		f.write( str(timestep) )
		f.close()

	a = date(2020, 9, 1)
	b = date.today()
	gap = b - a
	gap = int(gap.days)
	date_list = []
	for z in range(0, gap+1, timestep):
		p = a + timedelta(days=z)
		p = p.strftime("%d/%m")
		date_list.append(p)

	plt.bar(x, y, color=color)
	plt.xticks( range(0, k, timestep), date_list )
	plt.xlabel("data", fontsize = 14)
	plt.ylabel(ylabel, fontsize=14)
	plt.grid(linewidth=0.5, axis='y')
	plt.savefig("pantarei/" + filename + "_graph.png", dpi=300)
	plt.clf()

def vax(filename, color):

	path1 = 'pantarei/primadose_story.txt'
	path2 = 'pantarei/secondadose_story.txt'
	f1 = open(path1)
	f2 = open(path2)
	y1 = []
	y2 = []
	x = []
	k = -1
	for line in f1:
		if k != -1:
			y1.append( float(line) )
			x.append(k)
		k = k+1
	j = -1
	for line in f2:
		if j != -1:
			y2.append( float(line) )
		j = j+1
	f1.close()
	f2.close()

	f = open("timestep_vax.txt")	#diverso timestep perché iniziato molto dopo
	for line in f:
		timestep = int(line)
	f.close()
	if len( range(0, k, timestep) ) > 7:
		f = open("timestep_vax.txt", 'w')
		timestep = timestep + 1
		f.write( str(timestep) )
		f.close()
	a = date(2021, 1, 2)
	b = date.today()
	gap = b - a
	gap = int(gap.days)
	date_list = []
	for z in range(0, gap+1, timestep):
		p = a + timedelta(days=z)
		p = p.strftime("%d/%m")
		date_list.append(p)

	plt.plot(x, y1, color=color, label = "prime dosi")
	plt.plot(x, y2, color=color, linestyle='dashed', label = "seconde dosi")
	plt.xticks( range(0, k, timestep), date_list )
	plt.xlabel("data", fontsize = 14)
	plt.legend()
	plt.grid(linewidth=0.5)
	f = mticker.ScalarFormatter(useOffset=False, useMathText=True)
	g = lambda x,pos : "${}$".format(f._formatSciNotation('%1.10e' % x))
	plt.gca().yaxis.set_major_formatter(mticker.FuncFormatter(g))
	plt.savefig("pantarei/" + filename + "_graph.png", dpi=300)
	plt.clf()