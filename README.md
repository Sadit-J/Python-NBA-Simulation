Sadit's NBA Simulation
----------------------

The program utilizes a database from Kaggle (https://www.kaggle.com/datasets/vivovinco/2023-2024-nba-player-stats) to simulate
an NBA game between two teams in the 2023-2024 playoffs. The information was imported to a MySQL database which was 
connected to Python via a MySQL extension.

The database contains information about each player's shooting percentages and basic stats. The information for each player was
stored within a classes which contained attributes for each part of a player's game such as their three point shooting or 
free throws. 

To simulate the outcome of a possession or a shot, the program utilized NumPy's library alongside python's Random library 
to create weighted options between the outcomes. Depending on the randomly generated the number, a certain outcome would be 
chosen which would lead to other possible events such as a foul or turnover. 



