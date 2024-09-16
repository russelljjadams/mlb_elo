import csv

def expected_score(rating_a, rating_b):
    return 1 / (1 + 10 ** ((rating_b - rating_a) / 400))

def load_games(filename):
    games = []
    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            games.append(row)
    return games

def update_elo_without_mov(rating, actual_score, expected_score, k=8):  # Increased K-factor
    return rating + k * (actual_score - expected_score)

def update_elo(rating, actual_score, expected_score, margin_of_victory, elo_diff, k=32):
    multiplier = ((margin_of_victory + 3) ** 1.0) / (5.0 + 0.003 * elo_diff)
    if margin_of_victory <= 2:
        multiplier = 1.5 * multiplier  # Boost Elo adjustments for close games
    return rating + k * multiplier * (actual_score - expected_score)

def calculate_elo(games, team_to_track="Arizona D'Backs"):
    teams = {}
    initial_elo = 1500  # Standard initial Elo
    k = 32  # K-Factor for more rapid adjustment
    home_field_advantage = 24  # Home field advantage

    for game in games:
        team1 = game['Team1']
        team2 = game['Team2']
        team1_runs = int(game['Team1_Runs'])
        team2_runs = int(game['Team2_Runs'])
        is_home_team2 = True  # Assuming Team2 is the home team

        # Initialize teams if needed
        teams.setdefault(team1, initial_elo)
        teams.setdefault(team2, initial_elo)

        # Determine winner, loser, and margin of victory
        if team1_runs > team2_runs:
            winner, loser = team1, team2
            margin_of_victory = team1_runs - team2_runs
            actual_score_winner, actual_score_loser = 1, 0
        else:
            winner, loser = team2, team1
            margin_of_victory = team2_runs - team1_runs
            actual_score_winner, actual_score_loser = 1, 0

        # Add home-field advantage to the home team’s Elo rating
        team1_adjusted = teams[team1]
        team2_adjusted = teams[team2] + home_field_advantage  # Apply home field advantage to Team2

        # Calculate expected scores
        expected_winner = expected_score(teams[winner], teams[loser])
        expected_loser = expected_score(teams[loser], teams[winner])

        # Calculate Elo difference
        elo_diff = abs(teams[team1] - teams[team2])

        # Update Elo ratings with margin of victory
        new_winner_elo = update_elo(teams[winner], actual_score_winner, expected_winner, margin_of_victory, elo_diff, k)
        new_loser_elo = update_elo(teams[loser], actual_score_loser, expected_loser, margin_of_victory, elo_diff, k)

        # Update the ratings
        teams[winner] = new_winner_elo
        teams[loser] = new_loser_elo

        # Only print Elo details if the game involves the Arizona Diamondbacks
        if team1 == team_to_track or team2 == team_to_track:
            print(f"Before game: {team1} (Elo: {teams[team1]:.2f}) vs {team2} (Elo: {teams[team2]:.2f})")
            print(f"Game result: {team1} ({team1_runs}) vs {team2} ({team2_runs})")
            print(f"Margin of Victory: {margin_of_victory}")
            print(f"Expected: {winner}={expected_winner:.4f}, {loser}={expected_loser:.4f}")
            print(f"New Elo: {winner}={new_winner_elo:.2f}, {loser}={new_loser_elo:.2f}\n")

    return teams




def predict_outcomes(today_games, elo_ratings):
    home_field_advantage = 24  # Elo points added to the home team
    predictions = []
    
    for game in today_games:
        team1, team2 = game
        rating1 = elo_ratings.get(team1, 1500)
        rating2 = elo_ratings.get(team2, 1500)

        # Apply home field advantage to the home team
        rating2_with_home_adv = rating2 + home_field_advantage

        prob1 = expected_score(rating1, rating2_with_home_adv)
        prob2 = 1 - prob1

        margin_of_victory1 = 7 * (prob1 - 0.5)
        margin_of_victory2 = 7 * (prob2 - 0.5)

        if prob1 > prob2:
            winner = team1
            margin = margin_of_victory1
        else:
            winner = team2
            margin = margin_of_victory2

        predictions.append({
            "Game": f"{team1} @ {team2}",
            "Projected Winner": winner,
            "Win Probability": f"{max(prob1, prob2):.2%}",
            "Expected Margin of Victory": f"{abs(margin):.2f} runs"
        })

    return predictions

# Load the historical games and calculate Elo ratings
games = load_games('data/mlb_games.csv')
elo_ratings = calculate_elo(games)

# Print the final Elo ratings for all teams
print("Final Elo Ratings:")
for team, rating in elo_ratings.items():
    print(f"{team}: {rating:.2f}")

def load_today_games(filename):
    today_games = []
    with open(filename, 'r') as file:
        lines = file.readlines()
        for line in lines:
            if '@' in line:
                parts = line.strip().split(' @ ')
                team1 = ' '.join(parts[0].split()[-2:])
                team2 = ' '.join(parts[1].split()[:2])
                today_games.append((team1, team2))
    return today_games

# Example usage:
# Load today's games from file and predict outcomes
today_games = load_today_games('todays_games.txt')
predictions = predict_outcomes(today_games, elo_ratings)

# Print predictions
for prediction in predictions:
    print(f"Game: {prediction['Game']}")
    print(f"Projected Winner: {prediction['Projected Winner']}")
    print(f"Win Probability: {prediction['Win Probability']}")
    print(f"Expected Margin of Victory: {prediction['Expected Margin of Victory']}")
    print()

