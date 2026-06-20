# TODO: STUDENT IMPLEMENTATION
import math
import time

class MinimaxAgent:
    def __init__(self, depth=4):
        self.depth = depth

    def evaluate(self, game, player):
        opponent = -player
        
        #  بررسی وضعیت پایان بازی 
        if game.game_over():
            scores = game.score()
            if isinstance(scores, dict):
                my_score = scores.get(player, 0)
                opp_score = scores.get(opponent, 0)
            elif isinstance(scores, (tuple, list)):
                my_score = scores[0] if player == 1 else scores[1]
                opp_score = scores[1] if player == 1 else scores[0]
            else:
                my_score, opp_score = 0, 0
                
            if my_score > opp_score: return 1000000
            elif my_score < opp_score: return -1000000
            else: return 0

        # ۲. استخراج اطلاعات بازی
        my_moves = len(game.get_valid_moves(player))
        opp_moves = len(game.get_valid_moves(opponent))
        
        scores = game.score()
        if isinstance(scores, dict):
            my_pieces = scores.get(player, 0)
            opp_pieces = scores.get(opponent, 0)
        elif isinstance(scores, (tuple, list)):
            my_pieces = scores[0] if player == 1 else scores[1]
            opp_pieces = scores[1] if player == 1 else scores[0]
        else:
            my_pieces, opp_pieces = 0, 0
            
        total_pieces = my_pieces + opp_pieces

        #  معیار تحرک Mobility
        if (my_moves + opp_moves) > 0:
            mobility = 100 * (my_moves - opp_moves) / (my_moves + opp_moves)
        else:
            mobility = 0

        #  معیار کنترل گوشه‌ها Corner Control
        try:
            rows = len(game.board)
            cols = len(game.board[0]) if rows > 0 else 0
            corners = [(0, 0), (0, cols - 1), (rows - 1, 0), (rows - 1, cols - 1)]
            
            my_corners = 0
            opp_corners = 0
            for r, c in corners:
                if game.board[r][c] == player:
                    my_corners += 1
                elif game.board[r][c] == opponent:
                    opp_corners += 1
                    
            if (my_corners + opp_corners) > 0:
                corner_weight = 100 * (my_corners - opp_corners) / (my_corners + opp_corners)
            else:
                corner_weight = 0
        except Exception:
            corner_weight = 0

        # معیار توازن مهره‌ها 
        if total_pieces > 0:
            coin_parity = 100 * (my_pieces - opp_pieces) / total_pieces
        else:
            coin_parity = 0

        #  وزن‌دهی پویا بر اساس درصد پر شدن صفحه 
        board_capacity = 0
        try:
            board_capacity = len(game.board) * len(game.board[0])
        except:
            board_capacity = 64
            
        fill_ratio = total_pieces / board_capacity if board_capacity > 0 else 0
        
        if fill_ratio < 0.35: # اوایل بازی
            w_coin, w_mobility, w_corner = 1, 5, 8
        elif fill_ratio < 0.65: # اواسط بازی
            w_coin, w_mobility, w_corner = 2, 4, 8
        else: # اواخر بازی
            w_coin, w_mobility, w_corner = 5, 1, 8

        final_score = (w_coin * coin_parity + w_mobility * mobility + w_corner * corner_weight) / (w_coin + w_mobility + w_corner)
        return final_score

    def minimax(self, game, depth, maximizing, root_player):
        current_player = root_player if maximizing else -root_player
        
        # شرط توقف
        if depth == 0 or game.game_over():
            return self.evaluate(game, root_player), None

        valid_moves = game.get_valid_moves(current_player)

        if not valid_moves:
            return self.minimax(game, depth - 1, not maximizing, root_player)

        if maximizing:
            max_eval = -math.inf
            best_move = valid_moves[0] if valid_moves else None
            for move in valid_moves:
                game_copy = game.copy()
                game_copy.make_move(current_player, move[0], move[1])
                eval_score, _ = self.minimax(game_copy, depth - 1, False, root_player)
                if eval_score > max_eval:
                    max_eval = eval_score
                    best_move = move
            return max_eval, best_move
        else:
            min_eval = math.inf
            best_move = valid_moves[0] if valid_moves else None
            for move in valid_moves:
                game_copy = game.copy()
                game_copy.make_move(current_player, move[0], move[1])
                eval_score, _ = self.minimax(game_copy, depth - 1, True, root_player)
                if eval_score < min_eval:
                    min_eval = eval_score
                    best_move = move
            return min_eval, best_move

    def choose_move(self, game, player):
        start_time = time.time()
        value, move = self.minimax(game, self.depth, True, player)
        end_time = time.time()
        # print(f"[{self.__class__.__name__}] Time taken: {end_time - start_time:.4f} seconds")
        return move