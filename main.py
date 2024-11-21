import discord
from discord.ext import commands
from discord import app_commands
import allteamwinloss, pointdifferential, StatOverTime
f = open("token.txt", "r")
TOKEN = f.read()
client = commands.Bot(command_prefix='!', intents=discord.Intents.all())


@client.event
async def on_ready():
	await client.tree.sync()
	print("Ready!")


@client.tree.command(
	name='winlossgraph',
	description='Gives the win/loss record'
)
async def win_loss(interaction, season: int = 5, team: str = 'all'):
	allteamwinloss.getwinloss(season, team)
	await interaction.response.send_message(file=discord.File('graph.png'))


@win_loss.autocomplete('team')
async def team_autocomplete(interaction, current: str):
	data = []
	for i in ['Portland Sunsets', 'Baltimore Mob', 'New York Rats', 'Pacific Ocean Prawns', 'Dublin Seasons',
	          'Transports', 'Kansas City Mints', 'Fresno Femboys', 'Seattle Seals', 'Boston Bee Boys',
	          'Denver Killers',
	          'Sox Puppets']:
		if current.lower() in i.lower():
			data.append(app_commands.Choice(name=i, value=i))
	return data


@client.tree.command(
	name='teamstatgraph',
	description='Gives the stat of a team over time'
)
async def team_stat(interaction, stat: str = 'curVibe', team: str = 'all', season: int = 5):
	StatOverTime.getTeamStat(stat, team, season)
	await interaction.response.send_message(file=discord.File('graph.png'))


@team_stat.autocomplete('stat')
async def stat_autocomplete(interaction, current: str):
	data = []
	for i in ['curVibe', "spiritFund", "seasonRunsAllowed", "seasonRunsScored"]:
		if current.lower() in i.lower():
			data.append(app_commands.Choice(name=i, value=i))
	return data


@team_stat.autocomplete('team')
async def team_autocomplete(interaction, current: str):
	data = []
	for i in ['Portland Sunsets', 'Baltimore Mob', 'New York Rats', 'Pacific Ocean Prawns', 'Dublin Seasons',
	          'Transports', 'Kansas City Mints', 'Fresno Femboys', 'Seattle Seals', 'Boston Bee Boys',
	          'Denver Killers',
	          'Sox Puppets']:
		if current.lower() in i.lower():
			data.append(app_commands.Choice(name=i, value=i))
	return data


client.run(TOKEN)
