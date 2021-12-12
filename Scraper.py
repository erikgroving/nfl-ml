import pandas as pd
import math

counter = 0

class Team:
	idCounter = 0
	idToTeam = {}
	def __init__(self, name, statsUrl):
		self.name = name 
		self.statsUrl = statsUrl
		self.id = int(Team.idCounter)
		Team.idToTeam[self.id] = self.name
		Team.idCounter += 1

	def setSchedule(self, schedule):
		self.schedule = schedule
	
	
class Game:
	def __init__(self, week, 
					opponent = None, 
					opponentName = None, 
					pointsFor = None, 
					pointsAgainst = None, 
					totalYards = None, 
					passYards = None, 
					rushYards = None, 
					turnovers = None, 
					defYdsAllowed = None, 
					defPassYards = None, 
					defRushYards = None, 
					defTurnovers = None, 
					awayGame = None):
		self.week = week
		self.opponent = opponent
		self.opponentName = opponentName
		self.pointsFor = pointsFor
		self.pointsAgainst = pointsAgainst
		self.totalYards = totalYards
		self.passYards = passYards
		self.rushYards = rushYards
		self.turnovers = turnovers
		self.defYdsAllowed = defYdsAllowed
		self.defPassYards = defPassYards
		self.defRushYards = defRushYards
		self.defTurnovers = defTurnovers
		self.awayGame = awayGame


class Scraper:

	def scrape(self):
		for _, team in self.teams.items():
			self.scrapeTeam(team)
		
		return self.teams

	def getOpponent(self, row, stats):
		return stats.at[row, ('Unnamed: 9_level_0', 'Opp')]

	def getPointsFor(self, row, stats):
		return stats.at[row, ('Score', 'Tm')]

	def getPointsAgainst(self, row, stats):
		return stats.at[row, ('Score', 'Opp')]

	def getTotalYards(self, row, stats):
		return stats.at[row, ('Offense', 'TotYd')]

	def getPassYards(self, row, stats):
		return stats.at[row, ('Offense', 'PassY')]
	
	def getRushYards(self, row, stats):
		return stats.at[row, ('Offense', 'RushY')]

	def getTurnovers(self, row, stats):
		to = stats.at[row, ('Offense', 'TO')]
		if pd.isna(to):
			to = 0
		return to 
	
	def getDefYardsAllowed(self, row, stats):
		return stats.at[row, ('Defense', 'TotYd')]
	
	def getDefPassYards(self, row, stats):
		return stats.at[row, ('Defense', 'PassY')]
	
	def getDefRushYards(self, row, stats):
		return stats.at[row, ('Defense', 'RushY')]
	
	def getDefTurnovers(self, row, stats):
		to = stats.at[row, ('Defense', 'TO')]
		if pd.isna(to):
			to = 0
		return to

	def isByeWeek(self, row, stats):
		return stats.at[row, ('Unnamed: 9_level_0', 'Opp')] == 'Bye Week'
	
	def isAwayGame(self, row, stats):
		return 1 if stats.at[row, ('Unnamed: 8_level_0', 'Unnamed: 8_level_1')] == '@' else 0

	def scrapeTeam(self, team):
		stats = pd.read_html(team.statsUrl + '2021.htm')[1]
		row = 0
		schedule = []
		while row < 18:
			opponentName = self.getOpponent(row, stats).split(' ')[-1]
			if self.isByeWeek(row, stats):
				game = Game(row, opponentName=opponentName)
				schedule.append(game)
				row += 1
				continue

			opponent = self.teams[self.getOpponent(row, stats).split(' ')[-1]].id
			pointsFor = self.getPointsFor(row, stats)
			pointsAgainst = self.getPointsAgainst(row, stats)
			totalYards = self.getTotalYards(row, stats)
			passYards = self.getPassYards(row, stats)
			rushYards = self.getRushYards(row, stats)
			turnovers = self.getTurnovers(row, stats)
			defYdsAllowed = self.getDefYardsAllowed(row, stats)
			defPassYards = self.getDefPassYards(row, stats)
			defRushYards = self.getDefRushYards(row, stats)
			defTurnovers = self.getDefTurnovers(row, stats)
			awayGame = self.isAwayGame(row, stats)

			game = Game(row, opponent, opponentName, pointsFor, pointsAgainst, totalYards, passYards, rushYards, turnovers, defYdsAllowed, defPassYards, defRushYards, defTurnovers, awayGame)
			schedule.append(game)

			row += 1
		team.setSchedule(schedule)


	def __init__(self):

		self.teams = {}

		cardinals = Team('Cardinals', 'https://www.pro-football-reference.com/teams/crd/')
		falcons = Team('Falcons', 'https://www.pro-football-reference.com/teams/atl/')
		ravens = Team('Ravens', 'https://www.pro-football-reference.com/teams/rav/')
		bills = Team('Bills', 'https://www.pro-football-reference.com/teams/buf/')
		panthers = Team('Panthers', 'https://www.pro-football-reference.com/teams/car/')		
		bears = Team('Bears', 'https://www.pro-football-reference.com/teams/chi/')
		bengals = Team('Bengals', 'https://www.pro-football-reference.com/teams/cin/')
		browns = Team('Browns', 'https://www.pro-football-reference.com/teams/cle/')
		cowboys = Team('Cowboys', 'https://www.pro-football-reference.com/teams/dal/')
		broncos = Team('Broncos', 'https://www.pro-football-reference.com/teams/den/')
		lions = Team('Lions', 'https://www.pro-football-reference.com/teams/det/')
		packers = Team('Packers', 'https://www.pro-football-reference.com/teams/gnb/')
		colts = Team('Colts', 'https://www.pro-football-reference.com/teams/clt/')
		texans = Team('Texans', 'https://www.pro-football-reference.com/teams/htx/')
		jaguars = Team('Jaguars', 'https://www.pro-football-reference.com/teams/jax/')
		chiefs = Team('Chiefs', 'https://www.pro-football-reference.com/teams/kan/')
		raiders = Team('Raiders', 'https://www.pro-football-reference.com/teams/rai/')
		chargers = Team('Chargers', 'https://www.pro-football-reference.com/teams/sdg/')
		rams = Team('Rams', 'https://www.pro-football-reference.com/teams/ram/')
		dolphins = Team('Dolphins', 'https://www.pro-football-reference.com/teams/mia/')
		vikings = Team('Vikings', 'https://www.pro-football-reference.com/teams/min/')
		patriots = Team('Patriots', 'https://www.pro-football-reference.com/teams/nwe/')
		saints = Team('Saints', 'https://www.pro-football-reference.com/teams/nor/')
		giants = Team('Giants', 'https://www.pro-football-reference.com/teams/nyg/')
		jets = Team('Jets', 'https://www.pro-football-reference.com/teams/nyj/')
		eagles = Team('Eagles', 'https://www.pro-football-reference.com/teams/phi/')
		steelers = Team('Steelers', 'https://www.pro-football-reference.com/teams/pit/')
		niners = Team('49ers', 'https://www.pro-football-reference.com/teams/sfo/')
		seahawks = Team('Seahawks', 'https://www.pro-football-reference.com/teams/sea/')
		buccaneers = Team('Buccaneers', 'https://www.pro-football-reference.com/teams/tam/')
		titans = Team('Titans', 'https://www.pro-football-reference.com/teams/oti/')
		wft = Team('Team', 'https://www.pro-football-reference.com/teams/was/')
		self.teams[cardinals.name] = cardinals
		self.teams[falcons.name] = falcons
		self.teams[ravens.name] = ravens 
		self.teams[bills.name] = bills 
		self.teams[panthers.name] = panthers 
		self.teams[bears.name] = bears
		self.teams[bengals.name] = bengals 
		self.teams[browns.name] = browns 
		self.teams[cowboys.name] = cowboys
		self.teams[broncos.name] = broncos 
		self.teams[lions.name] = lions
		self.teams[packers.name] = packers 
		self.teams[colts.name] = colts
		self.teams[texans.name] = texans
		self.teams[jaguars.name] = jaguars
		self.teams[chiefs.name] = chiefs
		self.teams[raiders.name] = raiders
		self.teams[chargers.name] = chargers
		self.teams[rams.name] = rams
		self.teams[dolphins.name] = dolphins
		self.teams[vikings.name] = vikings
		self.teams[patriots.name] = patriots
		self.teams[saints.name] = saints
		self.teams[giants.name] = giants
		self.teams[jets.name] = jets
		self.teams[eagles.name] = eagles
		self.teams[steelers.name] = steelers
		self.teams[niners.name] = niners
		self.teams[seahawks.name] = seahawks
		self.teams[buccaneers.name] = buccaneers
		self.teams[titans.name] = titans
		self.teams[wft.name] = wft