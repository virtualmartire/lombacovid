from matplotlib import pyplot as plt
import matplotlib.ticker as mticker
from matplotlib.dates import drange, DateFormatter
from datetime import date, timedelta
import json

def curve(label, filename, color, ylabel, path='pantarei/story.json'):

	with open(path) as story_json_file:
		story_dict = json.load(story_json_file)

	y = story_dict[label]

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

def histo(label, filename, color, ylabel, path='pantarei/story.json'):

	with open(path) as story_json_file:
		story_dict = json.load(story_json_file)

	y_bars = story_dict[label]
    
	y_fit = y_bars.copy()
	for i in range(2, len(y_fit)-2):
		y_fit[i] = (y_bars[i-2] + y_bars[i-1] + y_bars[i] + y_bars[i+1] + y_bars[i+2]) / 5

	formatter = DateFormatter('%d/%m')
	a = date(2020, 9, 1)
	b = date.today() + timedelta(days=1)
	delta = timedelta(days=1)
	dates = drange(a, b, delta)

	plt.plot(dates, y_fit, color=color, label="media mobile")
	plt.bar(dates, y_bars, color="#9fcef9", label="val. assoluto")
	plt.gca().xaxis_date()
	plt.xlabel("data", fontsize = 14)
	plt.gca().xaxis.set_major_formatter(formatter)
	plt.ylabel(ylabel, fontsize=14)
	plt.grid(linewidth=0.5, axis='y')
	plt.legend()
	plt.savefig("pantarei/" + filename + "_graph.png", dpi=300)
	plt.clf()

def vax(filename, color, path='pantarei/story.json'):

	with open(path) as story_json_file:
		story_dict = json.load(story_json_file)

	y1 = story_dict['primadose_story']
	y2 = story_dict['secondadose_story']

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