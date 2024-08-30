class personal_info:
    def __init__(self, full_name, team):
        self.name = full_name
        self.team = team


class three_pt:
    def __init__(self, threepm, threepa, threepct):
        self.threepm = float(threepm)
        self.threepa = float(threepa)
        self.threepct = float(threepct)

class two_pt:
    def __init__(self, twopm, twopa, twopct):
        self.twopm = float(twopm)
        self.twopa = float(twopa)
        self.twopct = float(twopct)
        
class ft_pt:
    def __init__(self, ftm, fta, ftpct):
        self.ftm = float(ftm)
        self.fta = float(fta)
        self.ftpct = float(ftpct)

class box_score:
     def __init__(self, orebounds, rebounds, assists, steals, blocks, turnovers, fouls, points):
        self.orebounds = float(orebounds)
        self.rebounds = float(rebounds)
        self.assists = float(assists)
        self.steals = float(steals)
        self.blocks = float(blocks)
        self.turnovers = float(turnovers)
        self.fouls = float(fouls)
        self.points = float(points)

class field_goal:
    def __init__(self, fgm, fga, fgpct):
        self.fgm = float(fgm)
        self.fga = float(fga)
        self.fgpct = float(fgpct)

class ingame:
    def __init__(self):
        self.num_shots = 0
        self.shots_made = 0
        self.points_scored = 0
        self.fouls_committed = 0
        self.turnovers_made = 0
        self.ft_attempted = 0
        self.steals_successful = 0
        self.shots_blocked = 0

        self.player_oncourt = True

class player:
    def __init__(self, info, field_goal, three_point, two_point, free_throw, basic_stats):
        self.info = info
        self.field_goal = field_goal
        self.three_point = three_point
        self.two_point = two_point
        self.free_throw = free_throw
        self.basic_stats = basic_stats

        self.ingame_stats = ingame()

    def finalstats(self):
        print("-----------------------\n")
        print("Player:", self.info.name)
        print("Number of shots:", self.ingame_stats.num_shots)
        print("Shots made:", self.ingame_stats.shots_made)
        print("Points:", self.ingame_stats.points_scored)
        print("Fouls:", self.ingame_stats.fouls_committed)
        print("Free Throws:", self.ingame_stats.ft_attempted,"\n")
        

    
    def fouled_out(self):
        if (self.ingame_stats.fouls_committed == 6):
            self.ingame_stats.player_oncourt = False

    def shot_scored(self, points_scored):
        self.ingame_stats.points += points_scored
        self.ingame_stats.num_shots += 1

