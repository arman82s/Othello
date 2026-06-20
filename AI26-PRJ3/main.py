"""
University: University of Isfahan
Faculty: Mathematics and Statistics
Department: Computer Science
Course: Artificial Intelligence
Professor: Dr. Faria Nasiri Mofakham
TAs: MehrAzin Marzough, Mohammad Karimi, Anahita Honarmandian
Project: Adversarial Search in Othello (Minimax and Alpha-Beta Pruning)
"""

from agents.random_agent import RandomAgent
from agents.greedy_agent import GreedyAgent
from agents.minimax_agent import MinimaxAgent
from agents.alphabeta_agent import AlphaBetaAgent
from tournament import play_game

def run_tournament(agent1, agent2, agent1_name, agent2_name, num_games=20, size=6):
    wins = 0
    losses = 0
    draws = 0
    
    for i in range(num_games):
        #  جای بازیکن سفید و سیاه در هر بازی عوض می‌شود
        if i % 2 == 0:
            score_b, score_w = play_game(agent1, agent2, size=size)
            my_score, opp_score = score_b, score_w
        else:
            score_b, score_w = play_game(agent2, agent1, size=size)
            my_score, opp_score = score_w, score_b
            
        if my_score > opp_score:
            wins += 1
        elif my_score < opp_score:
            losses += 1
        else:
            draws += 1
            
    win_rate = (wins / num_games) * 100
    return wins, losses, draws, win_rate

if __name__ == "__main__":
    print("\n" + "="*65)
    print(f"{'Agent':<15} | {'Opponent':<10} | {'Games':<6} | {'Wins':<5} | {'Win Rate'}")
    print("-" * 65)

    matchups = [
        (MinimaxAgent(depth=4), RandomAgent(), "Minimax", "Random"),
        (MinimaxAgent(depth=4), GreedyAgent(), "Minimax", "Greedy"),
        (AlphaBetaAgent(depth=4), RandomAgent(), "Alpha-Beta", "Random"),
        (AlphaBetaAgent(depth=4), GreedyAgent(), "Alpha-Beta", "Greedy"),
    ]

    # اجرای مسابقات و چاپ نتایج
    for agent, opponent, a_name, o_name in matchups:
        w, l, d, wr = run_tournament(agent, opponent, a_name, o_name, num_games=20, size=6)
        print(f"{a_name:<15} | {o_name:<10} | {20:<6} | {w:<5} | {wr:.1f}%")

    print("="*65 + "\n")