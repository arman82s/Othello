from game.othello import Othello, BLACK, WHITE

def play_game(agent_black, agent_white, size=6):
    game = Othello(size)
    player = BLACK
    while not game.game_over():
        moves = game.get_valid_moves(player)
        if moves:
            agent = agent_black if player == BLACK else agent_white
            move = agent.choose_move(game, player)
            # اطمینان از اینکه عامل حرکتی را برگردانده است
            if move is not None:
                game.make_move(player, *move)
        # تغییر نوبت (اگر بازیکن حرکتی نداشته باشد، نوبت پاس می‌شود)
        if player == BLACK:
            player = WHITE
        else:
            player = BLACK
            
    return game.score()