import csv
import math

# Constants for adjustments
HOME_FIELD_ADVANTAGE = 24
TRAVEL_PENALTY_CONSTANT = -0.31
REST_BONUS = 2.3
DEFAULT_STARTING_PITCHER_ADJ = 0

def expected_score(rating_a, rating_b):
    return 1 / (1 + 10 ** ((rating_b - rating_a) / 400))

def update_elo(rating, actual_score, expected_score, margin_of_victory, elo_diff, k=30):
    multiplier = ((margin_of_victory + 3) ** 0.8) / (7.5 + 0.006 * elo_diff)
    return rating + k * multiplier * (actual_score - expected_score)

def apply_home_field_advantage(team_rating, is_home_team):
    if is_home_team:
        return team_rating + HOME_FIELD_ADVANTAGE
    return team_rating

def apply_travel_penalty(team_rating, miles_traveled):
    return team_rating + miles_traveled**(1.0/3.0) * TRAVEL_PENALTY_CONSTANT

def apply_rest_bonus(team_rating, days_of_rest):
    return team_rating + min(days_of_rest, 3) * REST_BONUS

def apply_pitcher_adjustment(team_rating, pitcher_adj):
    return team_rating + pitcher_adj

def load_games(filename):
    games = []
    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            games.append(row)
    return games

def calculate_elo(games):
    teams = {}  # Store Elo by team name
    k = 30

    for game in games:
        team1 = game['Team1']
        team2 = game['Team2']
        team1_runs = int(game['Team1_Runs'])
        team2_runs = int(game['Team2_Runs'])

        # Initialize teams if needed
        teams.setdefault(team1, 1500)
        teams.setdefault(team2, 1500)

        # Apply game adjustments
        team1_rating = apply_home_field_advantage(teams[team1], is_home_team=True)
        team2_rating = apply_home_field_advantage(teams[team2], is_home_team=False)

        # You could apply travel penalties and rest bonuses here if you have that data

        # Determine the winner
        if team1_runs > team2_runs:
            winner, loser = team1, team2
            margin_of_victory = team1_runs - team2_runs
        else:
            winner, loser = team2, team1
            margin_of_victory = team2_runs - team1_runs

        elo_diff = abs(teams[team1] - teams[team2])

        # Calculate expected scores
        expected_winner = expected_score(teams[winner], teams[loser])

        # Calculate Elo updates  
        teams[winner] = update_elo(teams[winner], 1, expected_winner, margin_of_victory, elo_diff, k)
        teams[loser] = update_elo(teams[loser], 0, 1 - expected_winner, margin_of_victory, elo_diff, k)

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

