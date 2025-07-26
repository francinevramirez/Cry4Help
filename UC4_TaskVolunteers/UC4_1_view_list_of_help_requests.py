import sqlite3
import flet as ft

def setup_database(db_path="cry4help.db"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS help_requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            requester_name TEXT,
            title TEXT,
            description TEXT,
            category TEXT,
            location TEXT,
            status TEXT
        )
    """)

    for column in ["category", "location", "status"]:
        try:
            cursor.execute(f"ALTER TABLE help_requests ADD COLUMN {column} TEXT")
        except sqlite3.OperationalError:
            pass

    conn.commit()
    conn.close()

# Connect to DB and Fetch Help Requests

def get_open_requests(db_path="cry4help.db"):
    setup_database(db_path)  # Only create table if not exists

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, requester_name, title, description, category, location
        FROM help_requests
        WHERE status = 'open'
        ORDER BY id ASC
    """)
    
    rows = cursor.fetchall()
    conn.close()
    return rows


# Flet UI to Display Help Requests

def main(page: ft.Page):
    page.title = "Cry4Help - Open Requests"
    page.scroll = ft.ScrollMode.AUTO
    page.window_width = 600
    page.window_height = 700
    page.bgcolor = ft.Colors.GREY_100

    requests = get_open_requests()

    if not requests:
        page.add(ft.Text("No open help requests at the moment.", color=ft.Colors.RED_600, size=18))
        return

    request_cards = []

    for r in requests:
        card = ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.Text(f"🔖 {r[2]}", size=20, weight="bold", color=ft.Colors.BLUE_900),
                    ft.Text(f"👤 Requested by: {r[1]}", size=14),
                    ft.Text(f"📝 Description: {r[3]}", size=14),
                    ft.Text(f"📚 Category: {r[4]}", size=14),
                    ft.Text(f"📍 Location: {r[5]}", size=14),
                ], spacing=5),
                padding=15,
                bgcolor=ft.Colors.WHITE,
                border_radius=10
            ),
            elevation=4
        )
        request_cards.append(card)

    page.add(
        ft.Column([
            ft.Text("📌 Available Help Requests", size=26, weight="bold", color=ft.Colors.BLUE_800),
            *request_cards
        ],
        spacing=15,
        alignment=ft.MainAxisAlignment.START,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER)
    )

ft.app(target=main)