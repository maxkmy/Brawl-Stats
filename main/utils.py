from datetime import datetime 
from matplotlib import pyplot as plt 
from matplotlib import dates as mpl_dates
import base64
from io import BytesIO

def getGraph(): 
	buffer = BytesIO() 
	plt.savefig(buffer, format='png')
	buffer.seek(0)
	imagePng = buffer.getvalue() 
	graph = base64.b64encode(imagePng)
	graph = graph.decode('utf-8')
	buffer.close()
	return graph 

def getPlot(dates, trophies): 
	plt.style.use('seaborn')
	plt.switch_backend('AGG')
	plt.figure(figsize=(11,5))
	plt.xlabel('date')
	plt.ylabel('trophies')
	plt.plot_date(dates, trophies, linestyle='solid')
	plt.tight_layout()
	plt.gcf().autofmt_xdate() 
	graph = getGraph()
	return graph