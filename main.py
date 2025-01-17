from Parse_Scrape import scraper, parser

"""
Only run these once each, as the web page will time you out for making too many requests

scraper("https://www.basketball-reference.com/leagues/NBA_{}_per_game.html", "all_players")
scraper("https://www.basketball-reference.com/awards/awards_{}.html", "awards")
scraper("https://www.basketball-reference.com/leagues/NBA_{}_standings.html", "standings")
parser("all_players", 'tr', ["thead","norank"], ["per_game_stats"], ["Players"],"data")

parser("awards", 'tr', ["thead", "over_header"], ["leading_all_nba", "leading_all_defense", "leading_all_rookie"], ["ALL-NBA", "ALL-DEF", "ALL-ROOK"], "team_awards")
parser("standings", 'tr', ["thead"], ["divs_standings_E"], ["Standings"],"data")


"""



parser("awards", 'tr', ["over_header"], ["mvp", "roy","dpoy", "smoy", "mip"], ["MVP", "ROY", "DPOY", "6MOY", "MIP"],"individual_awards")