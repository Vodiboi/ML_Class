import random
import flet as ft
from paper2048 import board, learning, pattern, move as Move
import time
import sys
sys.setrecursionlimit(int(1e9))

# Initialize backend lookup table

def main(page: ft.Page):
    page.title = "2048 with Model"
    page.window_width = 400
    page.window_height = 550
    # Keep original layout structure
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = 10
    page.theme_mode = "LIGHT"
    page.bgcolor = "#FAF8EF"

    # Backend game state
    board.lookup.init()
    state = board()
    state.init()
    score = 0

    # Reinforcement Learning model setup
    tdl = learning()
    tdl.add_feature(pattern([0, 1, 2, 3, 4, 5]))
    tdl.add_feature(pattern([4, 5, 6, 7, 8, 9]))
    tdl.add_feature(pattern([0, 1, 2, 4, 5, 6]))
    tdl.add_feature(pattern([4, 5, 6, 8, 9, 10]))
    tdl.load("2048.bin")

    # UI controls
    score_text = ft.Text(f"Score: {score}", size=20, weight="bold")
    esti_text = ft.Text(f"Estimated Value: {tdl.estimate(state):.2f}", size=16)
    best_move = ft.Text(f"Best Move: ")
    model_insight = ft.PopupMenuItem("")
    insight_menu =  ft.PopupMenuButton(icon=ft.Icons.INFO, items=[model_insight], tooltip=ft.Tooltip("Model Insight"))
    # def on_auto_play(e):

    auto_play = ft.Switch(label="Model Auto Play", on_change=lambda x: update_ui())
    
    # Color mapping for tiles
    tile_colors = {
        0: "#CDC1B4", 2: "#EEE4DA", 4: "#EDE0C8", 8: "#F2B179", 16: "#F59563",
        32: "#F67C5F", 64: "#F65E3B", 128: "#EDCF72", 256: "#EDCC61", 512: "#EDC850",
        1024: "#EDC53F", 2048: "#EDC22E",
    }

    # Create 4x4 grid of tiles
    tiles = []
    for i in range(16):
        tile = ft.Container(
            content=ft.Text("", size=24, weight="bold"),
            width=80,
            height=80,
            alignment=ft.alignment.center,
            bgcolor=tile_colors[0],
            border_radius=5,
            margin=5,
        )
        tiles.append(tile)
    rows = [ft.Row(controls=tiles[y*4:(y+1)*4], alignment=ft.MainAxisAlignment.CENTER) for y in range(4)]

    # Restart button
    def on_reset(e):
        nonlocal state, score
        state = board()
        state.init()
        score = 0
        update_ui()

    reset_button = ft.ElevatedButton(text="Restart", on_click=on_reset)

    # Handle arrow-key presses
    def on_key(e: ft.KeyboardEvent):
        nonlocal score
        key_map = {"Arrow Up": 0, "Arrow Right": 1, "Arrow Down": 2, "Arrow Left": 3}
        if e.key in key_map:
            reward = state.move(key_map[e.key])
            if reward >= 0:
                score += reward
                state.popup()
                update_ui()

    # Assemble the UI
    board_col = ft.Column(
        controls=[score_text, esti_text, best_move] + rows + [reset_button, insight_menu, ft.Row([auto_play], alignment=ft.MainAxisAlignment.CENTER)],
        spacing=10,
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    page.add(board_col)
    page.on_keyboard_event = on_key

    # UI update function
    def update_ui():
        # Update grid tiles
        for idx, tile in enumerate(tiles):
            exp = state.at(idx)
            val = 2**exp if exp > 0 else 0
            tile.content.value = str(val) if val > 0 else ""
            tile.bgcolor = tile_colors.get(val, "#3C3A32")
            tile.content.color = "#776E65" if val <= 4 else "#F9F6F2"

        # Update score and estimate
        score_text.value = f"Score: {score}"
        esti_text.value = f"Estimated Final Score: {tdl.estimate(state)+score:.2f}"

        # Compute model suggestions
        valid_moves = []
        for opcode in range(4):
            mv = Move(state, opcode)
            if mv.is_valid():
                mv.set_value(mv.reward() + tdl.estimate(mv.afterstate()))
                valid_moves.append(mv)
        if valid_moves:
            # Sort by value descending
            valid_moves.sort(key=lambda m: m.value(), reverse=True)
            best = valid_moves[0]
            # second = valid_moves[1] if len(valid_moves) > 1 else None
            # suggestion = f"{best.name()} ({best.value():.2f})"
            # if second:
            #     suggestion += f"; Next: {second.name()} ({second.value():.2f})"
            # move_dropdown.options = [
            #     ft.dropdown.Option(text=suggestion, key=str(best.action()))
            # ]
            # Keep closed view as hint
            # move_dropdown.value = None
            model_insight.text = "The model tries to predict the final score assuming optimal play for a given board state. Here is what the model thinks the final score will be, assuming the following moves are played:\n\n" + "\n".join([f"{x.name()} \t:\t {round(x.value()+score, 5)}" for x in valid_moves]) + f"\n\nHence, the model believes the best move is {best.name().lower()}"
            model_insight.update()
            best = max(valid_moves, key=lambda m: m.value())
            best_move.value = f"Best Move: {best.name()}"
            best_move.update()
        else:
            # Game over
            best_move.value = None
            model_insight.text = "The game is over."
            best_move.update()
            dlg = ft.AlertDialog(
                title=ft.Text("Game Over"),
                content=ft.Text(f"Final Score: {score}"),
                actions=[ft.TextButton("Restart", on_click=lambda e: [page.dialog.close(), on_reset(e)])]
            )
            page.dialog = dlg
            dlg.open = True

        page.update()
        keys = ["Arrow Up", "Arrow Right", "Arrow Down", "Arrow Left"]
        insight_menu.disabled = auto_play.value
        if auto_play.value and valid_moves:
            time.sleep(0.01)
            on_key(ft.KeyboardEvent(keys[best.action()], False, False, False, False))
        # ft.SafeArea()
        # page.on_app_lifecycle_state_change()

    # Initial render
    update_ui()


ft.app(target=main)
