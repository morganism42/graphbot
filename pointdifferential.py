import matplotlib.pyplot as plt
import requests


def getpointdiff(season=5, includePost=False, targ='all'):
	teamstemp = ['Portland Sunsets', 'Baltimore Mob', 'New York Rats', 'Pacific Ocean Prawns', 'Dublin Seasons',
	             'Transports', 'Kansas City Mints', 'Fresno Femboys', 'Seattle Seals', 'Boston Bee Boys',
	             'Denver Killers',
	             'Sox Puppets']
	if targ != 'all':
		if targ not in teamstemp:
			print('Team not found')
			return
		teamstemp = [targ]
	if season == 0:
		url = 'https://daseballapi.adaptable.app/games'
	else:
		url = 'https://daseballapi.adaptable.app/games/' + str(season)
	response = requests.get(url)
	data = response.json()
	teams = []
	number = -5
	for team in teamstemp:
		teams.append([team, '', [[number / 30, -1]]])
		number += 1
		for game in data:
			if game['homeTeam']['teamName'] == team:
				teams[-1][1] = game['homeTeam']['teamColor']
			elif game['awayTeam']['teamName'] == team:
				teams[-1][1] = game['awayTeam']['teamColor']
	for n, team in enumerate(teams):
		for game in data:
			if game['homeTeam']['gamesPlayed'] <= 20 or includePost:
				if game['homeTeam']['teamName'] == team[0]:
					teams[n][2].append([game['homeScore'] - game['awayScore'], game['gameDay']])
				elif game['awayTeam']['teamName'] == team[0]:
					teams[n][2].append([game['awayScore'] - game['homeScore'], game['gameDay']])
	for n, team in enumerate(teams):
		teams[n][2].sort(key=lambda x: x[1])
		teams[n][2][0] = teams[n][2][0][0]
		for x in range(1, len(teams[n][2])):
			teams[n][2][x] = teams[n][2][x - 1] + teams[n][2][x][0]
	for team in teams:
		plt.plot(team[2], label=team[0], color='#' + team[1], marker='$'+team[0][0]+'$', markersize=5)
	plt.legend(fontsize='x-small', loc='upper left')
	plt.xlabel('Game Number')
	plt.ylabel('Point Differential')
	plt.locator_params(axis='both', integer=True)
	plt.xticks(range(0, max([len(team[2]) for team in teams]), 2))
	ymax = int(max([max(team[2]) for team in teams]))
	ymin = int(min([min(team[2]) for team in teams]))
	ymin = ymin - (ymin % 5)
	ymax = ymax + (5 - ymax % 5)
	plt.yticks(range(ymin, ymax+1, 5))
	if targ != 'all':
		plt.title('Point differential for ' + targ)
	else:
		plt.title('Point differential for all teams')
	plt.grid()
	plt.margins(x=0)
	plt.savefig('graph.png')
	plt.close()