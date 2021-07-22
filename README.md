# dream11-selection
A model for helping select a team of 11 cricket players from a pool of 22 to form a Dream11 team for a single match.
The data set used contains match-wise ball to ball data of each IPL match from 2008 to 2020.
When selecting a team of 11 players from a pool of 22 players from both teams, it is desirable to select the players that will maximize the total points earned by the fantasy 11 team. The Dream11 points system takes into account all contributions a cricket player can make on the field using some stats like: runs, strike rate, boundaries, wickets, catches etc. 
As a first step, I have tried to predict the runs a batsman will score in the upcoming match. To make this prediction, the batsman's recent form and his stats against the bowlers of the opponent team can be taken into account.
## runner.ipynb
This is the notebook used to run the functions in the other python scripts.
## plotting.py
Contains a function called 'h2h_plot' which is used to create a plot of runs scored by a batsman in each previous match against a given bowler, strike rate in each of those matches and whether or not the bowler took the batsman's wicket.
As an example, Virat Kohli against Jasprit Bumrah is considered.
![head2head](https://user-images.githubusercontent.com/24764839/126683446-da5a21e3-bf29-49f6-a80c-f10ecc01aca7.png)
## calc_stats.py
Contains function h2h_stats which is used to obtain the statistics of each time the given batsman faced the given bowler. Match IDs, dates, venues are obtained along with balls faced and runs scored both against the bowler in particular and in the entire match where the batsman faced the bowler. It also contains information if the bowler got him out or not in each of the innings.
