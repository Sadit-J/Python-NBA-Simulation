# Programmer: Sadit Joarder
# Name: 
# Description: The program takes information of players who played in the 2023-2024
# playoffs and stores two rosters within a list. Each person is stored as a player object
# which is used to store their attributes. These players are matched to their teams to simulate
# a NBA playoff game between 2 teams



import mysql.connector
import random
import numpy as np

from NBA_Classes import *

def teamstats(roster):

    #Stores the sum of all basic box score stats from each player
    boxscore_stats = ["orebounds", "rebounds", "assists", "steals", "blocks", "turnovers", "fouls", "points"]
    team_stats = []
    
    
    player_stats = [person.basic_stats for person in roster]

    for stat in boxscore_stats:
        team_attribute = sum(getattr(per_player, stat) for per_player in player_stats)
        team_stats.append(team_attribute)

    return team_stats

#Receives the teams wanted by the user and takes the players on the
#roster from the nba database
def extracting_data(firstchosen_team, secondchosen_team):

    #Connecting to the nba database in MySql 
    nba_db = mysql.connector.connect(
     host="localhost",
     user="root",
     password="password?",
     database="nba"
    )

    mycursor = nba_db.cursor()

    # Selecting the Table With All The Data #
    mycursor.execute("SELECT * FROM nba_players")

    active_nba = mycursor.fetchall()

    roster_one = []
    roster_two = []

    #Iterates through each person in the database to check if they are playing
    #for the teams the user desires
    for person in active_nba:
        
        #Once the player fits the condition, multiple classes are used to construct
        #each player's object
        if (person[4] == firstchosen_team) or (person[4] == secondchosen_team):
            player_info = personal_info(person[1], person[4])
            field_goal_data = field_goal(person[8], person[9], person[10])
            three_point_data = three_pt(person[11], person[12], person[13])
            two_point_data = two_pt(person[14], person[15], person[16])
            free_throw_data = ft_pt(person[18], person[19], person[20])
            basic_stats = box_score(person[21], person[23], person[24], person[25], person[26], person[27], person[28], person[29])

            current_player = player(player_info, field_goal_data, three_point_data, 
                                    two_point_data, free_throw_data, basic_stats)
            
            #Puts each player on their respective team
            if (person[4] == firstchosen_team):
                roster_one.append(current_player)

            elif (person[4] == secondchosen_team):
                roster_two.append(current_player)

    #Stores the basic box scores stats for the entire team
    #such as rebounds, steals, etc
    teamone_average = teamstats(roster_one)
    teamtwo_average = teamstats(roster_two)
    
    #Once the data has been collected, the simulation is started
    simulation(roster_one, roster_two, teamone_average, teamtwo_average)
    

def calculate_posessions(player_stats, team_stats):

    #The calculation is based on the standard formula 
    #provided by ESPN to calculate average possession per team
    team_fga = 0
    team_fta = 0

    for player in player_stats:
        team_fga += player.field_goal.fga
        team_fta += player.free_throw.fta

    num_of_poss = 0.96*((team_fga)+(team_stats[5])+0.44*(team_fta)-(team_stats[0]))


    return int(num_of_poss)

def per_possession(current_team, opposing_team, possession):

    
    #The possible outcomes of the possession are the opposing team stealing the ball, blocking the shot,
    #a turnover or the opposing team fouling the offensive player
    posession_outcomes = [opposing_team[3], opposing_team[4], current_team[5], opposing_team[6]]
    
    #The final outcome added to the list is a regular possession which results in a shot
    posession_outcomes.append(possession - sum(posession_outcomes[0:3]) - posession_outcomes[0])


    
    #Utilizes weighted choices from the numpy library with a normalized list
    #to get the outcome of the possession
    normalized_outcomes = [float(x)/sum(posession_outcomes) for x in posession_outcomes]
    choice = np.random.choice(posession_outcomes, p=normalized_outcomes)

    final_outcome = posession_outcomes.index(choice) 

    return final_outcome

def select_player(roster, main_attribute, statistic):
    player_found = False

    #Weighted choices works similar to the finding the outcome of a possesssion
    attribute_list = [getattr(person, main_attribute) for person in roster]
    statistic_list  = [float(getattr(each_attribute, statistic)) for each_attribute in attribute_list]

    norm_list = [float(x)/sum(statistic_list) for x in statistic_list]

    #The function keeps looking for a player that is on court and has not
    #fouled out
    while (player_found == False):
        chosen = np.random.choice(statistic_list, p=norm_list)
        player_index = statistic_list.index(chosen)

        player_found = roster[player_index].ingame_stats.player_oncourt

    return player_index

#Once a player has been selected the function uses weighted choices
#to choose between a 2 pointer or 3 pointer
def shot_type(roster, player_index):

    shot_points = [2, 3]
    shot_type = [roster[player_index].two_point.twopa, roster[player_index].three_point.threepa]
    shot_pct = [roster[player_index].two_point.twopct, roster[player_index].three_point.threepct]

    try: 
        normalized_shot = [float(x)/sum(shot_type) for x in shot_type]

        shot_taken = np.random.choice(shot_points, p=normalized_shot)
        shot_index = shot_points.index(shot_taken)

        shot_chance = round(random.random(), 2)
       
        roster[player_index].ingame_stats.num_shots += 1

        if (shot_chance < shot_pct[shot_index]):

            roster[player_index].ingame_stats.points_scored += shot_taken
            roster[player_index].ingame_stats.shots_made += 1

    except:

        #If a player does not usually take a shot during a game, another
        #player is chosen
        select_player(roster, "field_goal", "fga")
        

#For each foul a player receives 2 free throws
def free_throws(roster, player_index):

    ft_pct = roster[player_index].free_throw.ftpct

    for x in range(2):
        free_throw_chance = round(random.random(), 2)
        if (free_throw_chance < ft_pct):
            roster[player_index].ingame_stats.points_scored += 1
    
    roster[player_index].ingame_stats.ft_attempted += 1


def final_output(roster_one, roster_two):

    teamone_score = 0
    for x in roster_one:
        teamone_score += x.ingame_stats.points_scored

    teamtwo_score = 0

    for x in roster_two:
        teamtwo_score += x.ingame_stats.points_scored    


    print("------- FINAL SCORE -------")
    print("    ",roster_one[0].info.team, teamone_score, " - ", teamtwo_score, roster_two[0].info.team)

    extra_information =  input("Would you like to see the individual statistics? (Y/N)\n").upper()

    if extra_information == "Y":

        print("\n-------",roster_one[0].info.team,"-------\n")
        for x in roster_one:
            x.finalstats()

        print("\n-------",roster_two[0].info.team,"-------\n")
        for x in roster_two:
            x.finalstats()

    simulate_again =  input("Would you like to simulate again? (Y/N)\n").upper()

    if simulate_again == "Y":
        main()
    

def simulation(roster_one, roster_two, teamone_stats, teamtwo_stats):

    team_one = [roster_one, teamone_stats, calculate_posessions(roster_one, teamone_stats)]
    team_two = [roster_two, teamtwo_stats, calculate_posessions(roster_two, teamtwo_stats)]
      
    total_possessions  = team_one[2] +  team_two[2]

    game_roster = [team_one, team_two]
    random.shuffle(game_roster)
    
    #The game is simulated for the average number of possessions in a game
    while (total_possessions > 0):

        #Based on the outcome of the possession, the players in game stats are updated
        possession_outcome = per_possession(game_roster[0][1], game_roster[1][1], game_roster[0][2])

        if possession_outcome == 0:
            player_index = select_player(game_roster[1][0], "basic_stats", "steals")
            game_roster[1][0][player_index].ingame_stats.steals_successful += 1

        elif possession_outcome == 1:
            player_index = select_player(game_roster[1][0], "basic_stats", "blocks")
            game_roster[1][0][player_index].ingame_stats.shots_blocked += 1

        elif possession_outcome == 2:
            player_index = select_player(game_roster[0][0], "basic_stats", "turnovers")
            game_roster[0][0][player_index].ingame_stats.turnovers_made += 1

        elif possession_outcome == 3:
            player_index = select_player(game_roster[1][0], "basic_stats", "fouls")
            game_roster[1][0][player_index].ingame_stats.fouls_committed += 1

            game_roster[1][0][player_index].fouled_out()

            player_index = select_player(game_roster[0][0], "free_throw", "fta")
            free_throws(game_roster[0][0], player_index)
        
        else:
            player_index = select_player(game_roster[0][0], "field_goal", "fga")
            shot_type(game_roster[0][0], player_index)

        game_roster.reverse()
        
        total_possessions -= 1

    final_output(game_roster[0][0], game_roster[1][0])


def main():
    team_one = input("Please enter the abbreviation of the first 2023-2024 playoff team (e.g: BOS, DEN, etc...)\n")
    team_two = input("Please enter the abbreviation of the second 2023-2024 playoff (e.g: BOS, DEN, etc...)\n")    
    
    extracting_data(team_one.upper(), team_two.upper())

main()

