from Parse_Scrape import scraper, parser
from Data_Clean import player_award_merge



#Only run these once each, as the web page will time you out for making too many requests or will try to overwrite large files

#Scrape
"""
scraper("https://www.basketball-reference.com/leagues/NBA_{}_per_game.html", "all_players")
scraper("https://www.basketball-reference.com/awards/awards_{}.html", "awards")
scraper("https://www.basketball-reference.com/leagues/NBA_{}_standings.html", "standings")
"""

#Parse
"""
parser("all_players", 'tr', ["thead","norank"], ["per_game_stats"], ["Players"],"data")
parser("awards", 'tr', ["thead", "over_header"], ["leading_all_nba", "leading_all_defense", "leading_all_rookie"], ["ALL-NBA", "ALL-DEF", "ALL-ROOK"], "team_awards")
parser("standings", 'tr', ["thead"], ["divs_standings_E"], ["Standings"],"data")
parser("awards", 'tr', ["over_header"], ["mvp", "roy","dpoy", "smoy", "mip"], ["MVP", "ROY", "DPOY", "6MOY", "MIP"],"individual_awards")

"""


#Clean
"""
player_award_merge("team_awards","ALL-NBA")
player_award_merge("team_awards","ALL-ROOK")
player_award_merge("team_awards","ALL-DEF")
player_award_merge("individual_awards","MVP")
player_award_merge("individual_awards","DPOY")
player_award_merge("individual_awards","6MOY")
player_award_merge("individual_awards","MIP")
player_award_merge("individual_awards","ROY")
"""






