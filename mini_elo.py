import csv

def expected_score(rating_a, rating_b):
    return 1 / (1 + 10 ** ((rating_b - rating_a) / 400)) 

# Simplified Elo update without margin of victory multiplier
def update_elo(rating, actual_score, expected_score, k=20):
    return rating + k * (actual_score - expected_score)

def load_games(filename):
    games = []
    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            games.append(row)
    return games

def calculate_elo(games):
    teams = {}  # Store Elo by team name
    k = 5 # Adjusted K-factor to reduce large rating swings
    for game in games:
        team1 = game['Team1']
        team2 = game['Team2']
        team1_runs = int(game['Team1_Runs'])
        team2_runs = int(game['Team2_Runs'])

        # Initialize teams if needed
        teams.setdefault(team1, 1500)
        teams.setdefault(team2, 1500)
        
        # Determine the winner and loser
        if team1_runs > team2_runs:
            winner, loser = team1, team2
            actual_score_winner = 1
        else:
            winner, loser = team2, team1
            actual_score_winner = 1
        
        # Calculate expected scores
        expected_winner = expected_score(teams[winner], teams[loser])
        expected_loser = 1 - expected_winner
        
        # Update Elo ratings
        teams[winner] = update_elo(teams[winner], actual_score_winner, expected_winner, k)
        teams[loser] = update_elo(teams[loser], 0, expected_loser, k)
        
        # Print game and rating updates
        print(f"Game: {team1} ({team1_runs}) vs {team2} ({team2_runs})")
        print(f"Expected score: {team1}={expected_score(teams[team1], teams[team2]):.4f}, {team2}={expected_score(teams[team2], teams[team1]):.4f}")
        print(f"New Elo ratings: {team1}={teams[team1]:.2f}, {team2}={teams[team2]:.2f}\n")
    
    return teams  # Dictionary of team names and final Elo

# Load the smaller test dataset
games = load_games('data/mlb_games.csv')
elo_ratings = calculate_elo(games)

# Print the final Elo ratings
print("Final Elo Ratings:")
print(elo_ratings)

