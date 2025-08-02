import sqlite3
import flet as ft

def setup_matches_table(db_path="cry4help.db"):
    """Creates the 'matches' table to store match history."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS matches (
        matchID INTEGER PRIMARY KEY AUTOINCREMENT,
        requestID INTEGER NOT NULL,
        volunteerID INTEGER NOT NULL, 
        match_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (requestID) REFERENCES help_requests (id)
    )
    ''')
    conn.commit()
    conn.close()

def store_match_info(request_id, volunteer_id, db_path="cry4help.db"):
    """
    This function handles the 'Store Match Info' task.
    It creates a match record and updates the request's status.
    """
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        # Step 1: Insert the new match into the 'matches' table
        cursor.execute(
            "INSERT INTO matches (requestID, volunteerID) VALUES (?, ?)",
            (request_id, volunteer_id)
        )
        # Step 2: Update the status of the request in the 'help_requests' table
        cursor.execute(
            "UPDATE help_requests SET status = 'Matched' WHERE id = ?",
            (request_id,)
        )
        conn.commit()
        conn.close()
        return True, "✅ Match successfully created!"
    except Exception as e:
        return False, f"❌ Database error: {e}"
        
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

    # --- # NEW: Setup both database tables when the app starts
    setup_database()
    setup_matches_table()
    
    # --- # NEW: Function to handle the 'Accept' button click
    def handle_accept_click(request_id, card_to_remove):
        # NOTE: In a real app, the volunteer_id would come from the logged-in user.
        # We will use a placeholder value of '1' for now.
        current_volunteer_id = 1 
        
        # This calls your "Store Match Info" function
        success, message = store_match_info(request_id, current_volunteer_id)

        # Show a confirmation message at the bottom of the screen
        page.snack_bar = ft.SnackBar(ft.Text(message))
        page.snack_bar.open = True
        
        # If the match was stored successfully, remove the card from the screen
        if success:
            request_list_view.controls.remove(card_to_remove)
        
        page.update()

    requests = get_open_requests()

    if not requests:
        page.add(ft.Text("No open help requests at the moment.", color=ft.colors.RED_600, size=18))
        return

    # --- # MODIFIED: The loop now creates an 'Accept' button on each card
    request_cards = []
    for r in requests:
        # We create the card variable first so we can pass it to the button's on_click handler
        card = ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.Text(f"🔖 {r[2]}", size=20, weight="bold", color=ft.colors.BLUE_900),
                    ft.Text(f"👤 Requested by: {r[1]}", size=14),
                    ft.Text(f"📝 Description: {r[3]}", size=14),
                    ft.Text(f"📚 Category: {r[4]}", size=14),
                    ft.Text(f"📍 Location: {r[5]}", size=14),
                    # --- # NEW: Add the "Accept" button to the card ---
                    ft.Container(
                        content=ft.ElevatedButton(
                            "Accept Request",
                            icon=ft.icons.CHECK_CIRCLE_OUTLINE,
                            # This lambda is important. It lets us pass the specific request ID
                            # and the card object itself to our handler function.
                            on_click=lambda _, req_id=r[0], c=card: handle_accept_click(req_id, c)
                        ),
                        alignment=ft.alignment.center_right,
                        margin=ft.margin.only(top=10)
                    )
                ], spacing=5),
                padding=15,
                bgcolor=ft.colors.WHITE,
                border_radius=10
            ),
            elevation=4
        )
        request_cards.append(card)

    # --- # NEW: Create a Column control that we can update later
    request_list_view = ft.Column(
        controls=request_cards,
        spacing=15,
        alignment=ft.MainAxisAlignment.START,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )

    page.add(
        ft.Column([
            ft.Text("📌 Available Help Requests", size=26, weight="bold", color=ft.colors.BLUE_800),
            request_list_view  # ... # MODIFIED: Add the new Column control here
        ],
        spacing=15,
        alignment=ft.MainAxisAlignment.START,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER)
    )

ft.app(target=main)
