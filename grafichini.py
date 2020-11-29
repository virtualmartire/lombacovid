from matplotlib import pyplot as plt
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