from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from .forms import PlayerForm
from .models import Player, Brawler
from .utils import getPlot
from datetime import datetime, date, timedelta
import requests

# brawl stars api calling 
headers = {
	"Accept": "application/json",
	"authorization": "your API key"
}

def getUser(playerTag): 
	urlRequest = "https://api.brawlstars.com/v1/players/%23" + str(playerTag)
	response = requests.get(urlRequest, headers)
	userJson = response.json()

	try: 
		name = userJson['name']
		trophies = userJson['trophies']
		experience = userJson['expLevel']

		brawlerList = []
		for brawler in userJson['brawlers']: 
			brawlerName = brawler['name']
			brawlerPower = brawler['power']
			brawlerRank = brawler['rank']
			brawlerTrophies = brawler['trophies']
			url = 'main/images/' + brawlerName + '.jpg'
			brawlerList.append([brawlerName, brawlerPower, brawlerRank, brawlerTrophies, url])

		return playerTag, name, trophies, experience, brawlerList

	except LookupError: 
		return None, None, None, None, None

# Create your views here.
def home(request): 
	if request.method == 'POST': 
		form = PlayerForm(request.POST) 
		if form.is_valid(): 
			obj = PlayerForm() 
			obj.playerTag = form.cleaned_data['playerTag']
			newUrl = 'display/' + str(obj.playerTag) + '/'
			return HttpResponseRedirect(newUrl)
		else: 
			return HttpResponse('<p>The form is not valid</p>')
	else: 
		form = PlayerForm()
		return render(request, 'main/home.html', {'playerForm':form})

def playerDetail(request, playerTag): 
	if request.method == 'POST': 
		form = PlayerForm(request.POST) 
		if form.is_valid(): 
			obj = PlayerForm() 
			obj.playerTag = form.cleaned_data['playerTag']
			newUrl = '/display/' + str(obj.playerTag) + '/'
			return HttpResponseRedirect(newUrl)
		else: 
			return HttpResponse('<p>The form is not valid</p>')
	else: 
		form = PlayerForm()
		# getting player and brawler information
		playerTag, name, trophies, experience, brawlerList = getUser(playerTag) 

		if name is None: 
			raise Http404("<p>The player tag does not exist. Player tags are case sensitive. Make sure to NOT include # in front of your player tag.</p>")

		playerSet = Player.objects.filter(playerTag=playerTag)
		if len(playerSet) == 1: 
			player = playerSet[0]
			today = str(date.today())
			datedTrophies = ' ' + today + ':' + str(trophies)
		else: 
			player = Player(playerTag=playerTag, trophies='') 
			today = str(date.today())
			datedTrophies = today + ':' + str(trophies)
		player.trophies = str(player.trophies) + str(datedTrophies) 
		player.save()

		datedTrophiesArr = player.trophies.split(' ')
		dates = []
		trophiesList = []
		for datedTrophy in datedTrophiesArr: 
			try:
				dateStr, trophy = datedTrophy.split(':')
				dates.append(dateStr)
				trophiesList.append(trophy)
			except ValueError: 
				pass
		trophiesList = list(map(float,trophiesList))
		chart = getPlot(dates,trophiesList)

		brawlerSet = Brawler.objects.filter(Player=player.id)
		for brawler in brawlerList: 
			brawlerName = brawler[0]
			newBrawler = True
			for brawlerObj in brawlerSet: 
				if brawlerName.upper() == brawlerObj.name.upper(): 
					datedTrophies = ' ' + str(date.today()) + ':' + str(brawler[3])
					brawlerObj.trophies = str(brawlerObj.trophies) + str(datedTrophies)
					newBrawler = False
					brawlerObj.save()
					break
			if newBrawler: 
				today = str(date.today())
				datedTrophies = today + ':' + str(brawler[3])
				brawlerObj = Brawler(name=brawlerName,trophies=datedTrophies, Player=player)
				brawlerObj.save()
			
		return render(request, 'main/playerDetail.html', {'playerTag':playerTag, 
													'playerName':name,
													'playerTrophies':trophies,
													'playerExperience':experience,
													'brawlerList': brawlerList,
													'chart': chart,
													'playerForm':form
													})


def brawlerDetail(request, playerTag, brawler): 
	playerSet = Player.objects.filter(playerTag=playerTag)
	player = playerSet[0]
	brawlerSet = Brawler.objects.filter(Player=player.id)

	for brawlerItem in brawlerSet: 
		if brawlerItem.name == brawler: 
			datedTrophiesArr = brawlerItem.trophies.split(' ')
			dates = []
			trophiesList = []
			for datedTrophy in datedTrophiesArr: 
				try: 
					dateStr, trophy = datedTrophy.split(':')
					dates.append(dateStr)
					trophiesList.append(trophy) 
				except ValueError: 
					pass 
			trophiesList = list(map(float,trophiesList))
			chart = getPlot(dates, trophiesList)
			break
	return render(request, 'main/brawlerDetail.html', {'chart':chart})
