import requests
import json
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties


def GetERA(data: list[dict], player):
	playerData = [[0, 0, 0]]
	for game in data:
		if game['homePitcher']['name'] == player:
			score = game['awayScore']
			innings = game['inningNumber']
			playerData.append([score + playerData[-1][0], innings + playerData[-1][1], game['gameDay']])
		elif game['awayPitcher']['name'] == player:
			score = game['homeScore']
			innings = game['inningNumber']
			playerData.append([score + playerData[-1][0], innings + playerData[-1][1], game['gameDay']])
	ERA = [0]
	gameday = [0]
	for game in playerData[1:]:
		ERA.append((9 * game[0]) / game[1])
		gameday.append(game[2])
	return [ERA, gameday]


def getPlayerStat(stat='ERA', player='Berry Sting', season=5):
	url = 'https://daseballapi.adaptable.app/games/' + str(season)
	response = requests.get(url)
	data = response.json()
	# print(data)
	if stat == 'ERA':
		value = GetERA(data, player)
		label = player + "'s ERA over season " + str(season)
		plt.plot(value[1], value[0])
		plt.title(label)
		plt.savefig('graph.png')
		plt.close()


def getTeamStat(stat='curVibe', targ='all', season=5):
	number = -10
	team = targ
	teamstemp = ['Portland Sunsets', 'Baltimore Mob', 'New York Rats', 'Pacific Ocean Prawns', 'Dublin Seasons',
	             'Transports', 'Kansas City Mints', 'Fresno Femboys', 'Seattle Seals', 'Boston Bee Boys',
	             'Denver Killers',
	             'Sox Puppets']
	if team != 'all':
		teamstemp = [team]
	url = 'https://daseballapi.adaptable.app/games/' + str(season)
	response = requests.get(url)
	data = response.json()
	teams = []
	for team in teamstemp:
		teams.append([team, ['', ''], [number / 30]])
		if team != 'all':
			teams[0][2] = [0]
		number += 2
		for game in data:
			if game['homeTeam']['teamName'] == team:
				teams[-1][1][0] = game['homeTeam']['teamColor']
				teams[-1][1][1] = game['homeTeam']['teamEmoji']
				break
			elif game['awayTeam']['teamName'] == team:
				teams[-1][1][0] = game['awayTeam']['teamColor']
				teams[-1][1][1] = game['homeTeam']['teamEmoji']
				break
	for n, team in enumerate(teams):
		for game in data:
			if game['homeTeam']['teamName'] == team[0]:
				teams[n][2].append(game['homeTeam'][stat] + team[2][0])
			elif game['awayTeam']['teamName'] == team[0]:
				teams[n][2].append(game['awayTeam'][stat] + team[2][0])
	for team in teams:
		plt.plot(team[2], label=team[0], color='#' + team[1][0], marker='$'+team[0][0]+'$', markersize=5)
	plt.title(stat + " over season " + str(season))
	plt.legend(fontsize='x-small', loc='upper left')
	plt.xlabel('Game Number')
	plt.ylabel(stat)
	plt.locator_params(axis='both', integer=True)
	if targ != 'all':
		plt.title(stat + ' for ' + targ)
	else:
		plt.title(stat + ' for all teams')
	plt.grid()
	plt.savefig('graph.png')
	plt.close()
