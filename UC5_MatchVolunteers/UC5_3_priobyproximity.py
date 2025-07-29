# Prioritize matches by proximity and availability of volunteer

import flet as ft
import requests

API_URL = "http://localhost:8000/match/prioritize"  

def main(page: ft.Page):
    page.title = "Prioritize Matches"
    page.window_width = 450
    page.window_height = 500
    page.vertical_alignment = "center"
    page.horizontal_alignment = "center"

    status = ft.Text("")
    matches_list = ft.Column([])

    def get_prioritized_matches(e):
        matches_list.controls.clear()
        try:
            resp = requests.post(API_URL)
            if resp.status_code == 200:
                matches = resp.json().get("matches", [])
                if matches:
                    for idx, match in enumerate(matches, 1):
                        volunteer = match.get("volunteer_email", "N/A")
                        distance = match.get("distance_km", "N/A")
                        available = "Available" if match.get("available", False) else "Unavailable"
                        matches_list.controls.append(
                            ft.Text(f"{idx}. {volunteer} | {distance:.2f} km | {available}")
                        )
                    status.value = "Matches prioritized by proximity and availability."
                    status.color = "green"
                else:
                    status.value = "No suitable volunteers found."
                    status.color = "red"
            else:
                status.value = f"Error: {resp.json().get('detail', 'Prioritization failed')}"
                status.color = "red"
        except Exception as ex:
            status.value = f"Error: {ex}"
            status.color = "red"
        page.update()

    page.add(
        ft.Column([
            ft.Text("Prioritize Matches by Proximity & Availability", size=20, weight="bold"),
            ft.ElevatedButton("Get Prioritized Matches", on_click=get_prioritized_matches),
            status,
            ft.Text("Matches:", size=16, weight="bold"),
            matches_list,
        ], alignment="center", horizontal_alignment="center")
    )

if __name__ == "__main__":
    ft.app(target=main)
