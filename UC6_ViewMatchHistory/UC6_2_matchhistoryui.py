# View Match History UI

import flet as ft
import requests

API_URL = "http://localhost:8000/match/history" 

def main(page: ft.Page):
    page.title = "Match History"
    page.window_width = 500
    page.window_height = 600
    page.vertical_alignment = "center"
    page.horizontal_alignment = "center"

    status = ft.Text("")
    history_list = ft.Column([])

    def get_match_history(e):
        history_list.controls.clear()
        try:
            resp = requests.get(API_URL)  # Changed to GET, no email sent
            if resp.status_code == 200:
                history = resp.json().get("history", [])
                if history:
                    for idx, match in enumerate(history, 1):
                        requester = match.get("requester_email", "N/A")
                        volunteer = match.get("volunteer_email", "N/A")
                        skill = match.get("skill", "N/A")
                        date = match.get("date", "N/A")
                        status_str = match.get("status", "N/A")
                        history_list.controls.append(
                            ft.Text(f"{idx}. Requester: {requester} | Volunteer: {volunteer} | Skill: {skill} | Date: {date} | Status: {status_str}")
                        )
                    status.value = "Match history loaded."
                    status.color = "green"
                else:
                    status.value = "No match history found."
                    status.color = "red"
            else:
                status.value = f"Error: {resp.json().get('detail', 'Could not retrieve history')}"
                status.color = "red"
        except Exception as ex:
            status.value = f"Error: {ex}"
            status.color = "red"
        page.update()

    page.add(
        ft.Column([
            ft.Text("View Match History", size=20, weight="bold"),
            ft.ElevatedButton("Show Match History", on_click=get_match_history),
            status,
            ft.Text("History:", size=16, weight="bold"),
            history_list,
        ], alignment="center", horizontal_alignment="center")
    )

if __name__ == "__main__":
    ft.app(target=main)
