# adopted from http://www.stanford.edu/class/cs224w/nx_tutorial.pdf

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pickle



if __name__ == '__main__' :	

	# insert file-name of data to be plotted
	b = 'RetweetedList100000.p'

	itemlist = pickle.load(open('{0}'.format(b), 'rb'))

	def plot_freq_dist(ls):
		counts = {}
		for n in ls:
			if n[1] not in counts:
				counts[n[1]] = 0
			counts[n[1]] += 1
		items = sorted(counts.items())
		fig = plt.figure()
		ax = fig.add_subplot(111)
		ax.plot ([ k for (k , v ) in items ] , [ v for (k ,v ) in items ])
		ax.set_xscale ('log')
		ax.set_yscale ('log')
		plt. title ("Degree Distribution")
		fig.savefig ("degree_distribution.png")




	# ------------- Function Calls -------------------------------

	plot_freq_dist(itemlist)