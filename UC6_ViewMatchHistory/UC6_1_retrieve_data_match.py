import sqlite3
from datetime import datetime
import flet as ft


def setup_match_history():
    conn = sqlite3.connect("cry4help.db")
    cursor = conn.cursor()

    # Force drop existing tables to prevent schema mismatch

    cursor.execute("DROP TABLE IF EXISTS match_history")
    cursor.execute("DROP TABLE IF EXISTS help_requests")

    # Recreate help_requests with required description field

    cursor.execute('''
        CREATE TABLE help_requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            requester_name TEXT NOT NULL,
            title TEXT NOT NULL,
            description TEXT NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE match_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            request_id INTEGER,
            volunteer_name TEXT NOT NULL,
            matched_on TEXT NOT NULL,
            status TEXT NOT NULL,
            FOREIGN KEY (request_id) REFERENCES help_requests(id)
        )
    ''')

    # Sample help requests with descriptions

    sample_requests = [
        ("Rafael", "Math Tutoring", "Needs help with algebra and solving equations."),
        ("Mia", "Computer Repair", "Laptop is not booting up after update.")
    ]
    for name, title, desc in sample_requests:
        cursor.execute(
            "INSERT INTO help_requests (requester_name, title, description) VALUES (?, ?, ?)",
            (name, title, desc)
        )
    # Fetch request IDs

    cursor.execute("SELECT id FROM help_requests")
    request_ids = [row[0] for row in cursor.fetchall()]

    # Sample match records

    sample_matches = [
        (request_ids[0], "Luke", "fulfilled"),
        (request_ids[1], "Isabel", "in progress")
    ]


    for req_id, vol, status in sample_matches:
        matched_on = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute('''
            INSERT INTO match_history (request_id, volunteer_name, matched_on, status)
            VALUES (?, ?, ?, ?)
        ''', (req_id, vol, matched_on, status))
    conn.commit()
    conn.close()

# Retrieve Match History

def retrieve_match_history():
    conn = sqlite3.connect("cry4help.db")
    cursor = conn.cursor()
    cursor.execute('''
        SELECT m.id, r.title, r.requester_name, m.volunteer_name, m.status, m.matched_on
        FROM match_history m
        JOIN help_requests r ON m.request_id = r.id
        ORDER BY m.matched_on DESC
    ''')
    records = cursor.fetchall()
    conn.close()
    return records


# Flet App: Match History Viewer


def main(page: ft.Page):
    page.title = "Cry4Help - Match History"
    page.scroll = ft.ScrollMode.AUTO
    page.window_width = 900
    page.window_height = 500
    page.bgcolor = ft.Colors.GREY_50

    setup_match_history()  
    records = retrieve_match_history()
    if not records:
        page.add(ft.Text("No match history found.", color=ft.Colors.RED_600, size=18))
        return
    table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Match ID")),
            ft.DataColumn(ft.Text("Request Title")),
            ft.DataColumn(ft.Text("Requester")),
            ft.DataColumn(ft.Text("Volunteer")),
            ft.DataColumn(ft.Text("Status")),
            ft.DataColumn(ft.Text("Matched On")),
        ],
        rows=[
            ft.DataRow(cells=[
                ft.DataCell(ft.Text(str(row[0]))),
                ft.DataCell(ft.Text(row[1])),
                ft.DataCell(ft.Text(row[2])),
                ft.DataCell(ft.Text(row[3])),
                ft.DataCell(ft.Text(row[4])),
                ft.DataCell(ft.Text(row[5])),
            ]) for row in records
        ]
    )
    page.add(
        ft.Column([
            ft.Text("📋 Match History", size=26, weight="bold", color=ft.Colors.BLUE_900),
            table
        ])
    )
ft.app(target=main)