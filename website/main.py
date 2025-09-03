import flet as ft
import requests
from collections import defaultdict
import random

data_raw = {
    "Aayan" : requests.get("http://www.aayanarish.com/ml_game_files/names_game.txt").text
}
data = {}
for (k, v) in data_raw.items():
    v2 = v.split("\n")
    v2.remove("")
    dct = {v2[i]:v2[i+1] for i in range(0, len(v2), 2)}
    data[k] = dct
score = defaultdict(int)
attempts = defaultdict(int)
home_screen = None

def changeView(pg:ft.Page, vw):
    pg.views.clear()
    pg.views.append(vw)
    pg.update()



def play_model(page, plr, model):
    answer = ft.Container(ft.Text(""))
    scorebrd = ft.Container(ft.Text(f"{score[(plr, model)]}/{attempts[(plr, model)]} = {score[(plr, model)]/attempts[(plr, model)] if attempts[(plr, model)] else 0}"))

    def updt_score():
        scorebrd.content = ft.Text(f"{score[(plr, model)]}/{attempts[(plr, model)]} = {score[(plr, model)]/attempts[(plr, model)] if attempts[(plr, model)] else 0}")
        # scorebrd.update()

    def reset_score(plr, model):
        score[(plr, model)] = 0
        attempts[(plr, model)] = 0
        answer.content = ft.Text("")
        updt_score()
        # scorebrd.update()
        regen()


    def wrong_answer(correct):
        nonlocal answer
        answer.content = ft.Text(f"Wrong, the correct answer was: {correct}")
        attempts[(plr, model)] += 1
        updt_score()
        # answer.update()
        regen()
    def right_answer():
        nonlocal answer
        answer.content = ft.Text(f"Correct!")
        score[(plr, model)] += 1
        attempts[(plr, model)] += 1
        updt_score()
        # answer.update()
        regen()

    def generate(amt_wrong=4):
        # a, b = data[plr][model], data[plr]["Real"]
        # for other way around:
        b, a = data[plr][model], data[plr]["Real"]
        a = a.split("|")
        b = b.split("|")
        correct = random.choice(b)
        lst = [
            ft.TextButton(x, on_click=lambda _: wrong_answer(correct))
            for x in random.sample(a, amt_wrong)
        ] + [
            ft.TextButton(correct, on_click=lambda _: right_answer())
        ]
        random.shuffle(lst)
        return lst

    def regen():
        lst = generate()
        vw = ft.View("", [
            ft.Column([
                ft.Row([
                    ft.IconButton(ft.icons.ARROW_BACK, on_click=lambda _: changeView(page, selectModelFromPlayer(page, plr))),
                    ft.IconButton(ft.icons.RESTART_ALT, on_click=lambda _: reset_score(plr, model)),
                    scorebrd
                ], alignment=ft.MainAxisAlignment.CENTER),
                ft.Row([
                    answer
                ], alignment=ft.MainAxisAlignment.CENTER),
                ft.Row([
                    ft.Text("Guess the Fake (4 are real, one is model generated):")
                ], alignment=ft.MainAxisAlignment.CENTER),
                ft.Row(lst, alignment=ft.MainAxisAlignment.CENTER)
            ])
        ])
        changeView(page, vw)
    regen()


    

def selectModelFromPlayer(page, plr):
    return ft.View("", [
        ft.Column([
            ft.Row([
                ft.IconButton(ft.icons.ARROW_BACK, on_click=lambda _: changeView(page, selectPlayerView(page))),
            ], alignment=ft.MainAxisAlignment.CENTER),
            ft.Row([
                ft.Text("Pick a Model:")
            ], alignment=ft.MainAxisAlignment.CENTER),
            ft.Row([
                ft.TextButton(k, on_click=lambda _: play_model(page, plr, k))
                for k, v in data[plr].items() if k != "Real"
            ], alignment=ft.MainAxisAlignment.CENTER)
        ])
    ])

def selectPlayerView(page):
    return ft.View("", [
        ft.Column([
            ft.Row([
                ft.IconButton(ft.icons.ARROW_BACK, on_click=lambda _: changeView(page, home_screen))
            ], alignment=ft.MainAxisAlignment.CENTER),
            ft.Row([
                ft.Text("Pick a Classmate to play against:")
            ], alignment=ft.MainAxisAlignment.CENTER)
        ] + [
            ft.Row([
                ft.TextButton(k, on_click=lambda _: changeView(page, selectModelFromPlayer(page, k)))
            ], alignment=ft.MainAxisAlignment.CENTER)
            for k, v in data.items()
        ])
    ])

def main(page: ft.Page):
    page.title = "ML Names game"
    global home_screen


    home_screen = ft.View("", [
        ft.Column([
            ft.Row([
                ft.Text("ML or Real: The Game")
            ], alignment=ft.MainAxisAlignment.CENTER),
            ft.Row([
                ft.TextButton("Click to Start", on_click=lambda _: changeView(page, selectPlayerView(page)))
            ], alignment=ft.MainAxisAlignment.CENTER)
        ])
    ])


    # def onNavigationChange(e):
    #     nonlocal cur_page

    #     changeView(page, cur_game())
    #     page.update()
    changeView(page, home_screen)

ft.app(target=main)