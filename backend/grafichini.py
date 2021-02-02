from matplotlib import pyplot as plt
import matplotlib.ticker as mticker
from matplotlib.dates import drange, DateFormatter
from datetime import date, timedelta

def curve(path, filename, color, ylabel):

	f = open(path)
	y = []
	for line in f:
		y.append( float(line) )
	f.close()

	#preparo l'array delle date
	formatter = DateFormatter('%d/%m')
	a = date(2020, 9, 1)
	b = date.today() + timedelta(days=1)
	delta = timedelta(days=1)
	dates = drange(a, b, delta)

	plt.plot_date(dates, y, color=color, linestyle='solid', marker=None)
	plt.xlabel("data", fontsize = 14)
	plt.gca().xaxis.set_major_formatter(formatter)
	plt.ylabel(ylabel, fontsize=14)
	plt.grid(linewidth=0.5)
	plt.savefig("pantarei/" + filename + "_graph.png", dpi=300)
	plt.clf()

def histo(path, filename, color, ylabel):

	f = open(path)
	y = []
	for line in f:
		y.append( float(line) )
	f.close()

	formatter = DateFormatter('%d/%m')
	a = date(2020, 9, 1)
	b = date.today() + timedelta(days=1)
	delta = timedelta(days=1)
	dates = drange(a, b, delta)

	plt.bar(dates, y, color=color)
	plt.gca().xaxis_date()
	plt.xlabel("data", fontsize = 14)
	plt.gca().xaxis.set_major_formatter(formatter)
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
	for line in f1:
		y1.append( float(line) )
	for line in f2:
		y2.append( float(line) )
	f1.close()
	f2.close()

	formatter = DateFormatter('%d/%m')
	a = date(2021, 1, 2)
	b = date.today() + timedelta(days=1)
	delta = timedelta(days=1)
	dates = drange(a, b, delta)

	plt.plot_date(dates, y1, color=color, linestyle='solid', marker=None, label = "prime dosi")
	plt.plot_date(dates, y2, color=color, linestyle='dashed', marker=None, label = "seconde dosi")
	plt.xlabel("data", fontsize = 14)
	plt.gca().xaxis.set_major_formatter(formatter)
	plt.legend()
	plt.grid(linewidth=0.5)
	f = mticker.ScalarFormatter(useOffset=False, useMathText=True)
	g = lambda x,pos : "${}$".format(f._formatSciNotation('%1.10e' % x))
	plt.gca().yaxis.set_major_formatter(mticker.FuncFormatter(g))
	plt.savefig("pantarei/" + filename + "_graph.png", dpi=300)
	plt.clf()