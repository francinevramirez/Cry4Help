import sqlite3
from datetime import datetime
import flet as ft
import csv  # NEW: Import the csv module

def setup_match_history():
    # ... (This function remains unchanged)
    conn = sqlite3.connect("cry4help.db")
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS match_history")
    cursor.execute("DROP TABLE IF EXISTS help_requests")
    cursor.execute('''CREATE TABLE help_requests (id INTEGER PRIMARY KEY, requester_name TEXT, title TEXT, description TEXT)''')
    cursor.execute('''CREATE TABLE match_history (id INTEGER PRIMARY KEY, request_id INTEGER, volunteer_name TEXT, matched_on TEXT, status TEXT, FOREIGN KEY (request_id) REFERENCES help_requests(id))''')
    sample_requests = [("Rafael", "Math Tutoring", "Needs help with algebra."),("Mia", "Computer Repair", "Laptop not booting.")]
    for name, title, desc in sample_requests:
        cursor.execute("INSERT INTO help_requests (requester_name, title, description) VALUES (?, ?, ?)",(name, title, desc))
    cursor.execute("SELECT id FROM help_requests")
    request_ids = [row[0] for row in cursor.fetchall()]
    sample_matches = [(request_ids[0], "Luke", "fulfilled"),(request_ids[1], "Isabel", "in progress")]
    for req_id, vol, status in sample_matches:
        matched_on = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute('INSERT INTO match_history (request_id, volunteer_name, matched_on, status) VALUES (?, ?, ?, ?)',(req_id, vol, matched_on, status))
    conn.commit()
    conn.close()

# --- MODIFIED: The function now accepts a filter ---
def retrieve_match_history(status_filter=None):
    conn = sqlite3.connect("cry4help.db")
    cursor = conn.cursor()
    sql = '''
        SELECT m.id, r.title, r.requester_name, m.volunteer_name, m.status, m.matched_on
        FROM match_history m
        JOIN help_requests r ON m.request_id = r.id
    '''
    params = []
    if status_filter and status_filter != "all":
        sql += " WHERE m.status = ?"
        params.append(status_filter)
    sql += " ORDER BY m.matched_on DESC"
    cursor.execute(sql, params)
    records = cursor.fetchall()
    conn.close()
    return records

# --- NEW: Function for your "History Export" task ---
def export_history_to_csv(datatable_rows):
    try:
        with open("match_history_export.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Match ID", "Request Title", "Requester", "Volunteer", "Status", "Matched On"])
            for row in datatable_rows:
                writer.writerow([cell.content.value for cell in row.cells])
        return True, "✅ History exported to match_history_export.csv"
    except Exception as e:
        return False, f"❌ Error during export: {e}"

# Flet App: Match History Viewer
def main(page: ft.Page):
    page.title = "Cry4Help - Match History"
    page.scroll = ft.ScrollMode.AUTO
    page.window_width = 900
    page.window_height = 600
    page.bgcolor = ft.colors.GREY_50

    setup_match_history()

    # --- UI Controls ---
    table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Match ID")),
            ft.DataColumn(ft.Text("Request Title")),
            ft.DataColumn(ft.Text("Requester")),
            ft.DataColumn(ft.Text("Volunteer")),
            ft.DataColumn(ft.Text("Status")),
            ft.DataColumn(ft.Text("Matched On")),
        ],
        rows=[] # Start with an empty table
    )
    
    # --- Event Handlers for your new features ---
    def update_table(status_filter=None):
        """Helper function to refresh the table with new data."""
        records = retrieve_match_history(status_filter)
        table.rows.clear() # Clear existing rows
        for row_data in records:
            table.rows.append(
                ft.DataRow(cells=[ft.DataCell(ft.Text(str(cell))) for cell in row_data])
            )
        page.update()
        
    def filter_changed(e):
        """Called when a radio button is clicked."""
        update_table(status_filter=e.control.value)

    def export_clicked(e):
        """Called when the export button is clicked."""
        success, message = export_history_to_csv(table.rows)
        page.snack_bar = ft.SnackBar(ft.Text(message))
        page.snack_bar.open = True
        page.update()

    # --- NEW: UI Controls for your tasks ---
    status_filter_radios = ft.RadioGroup(
        content=ft.Row([
            ft.Radio(value="all", label="All"),
            ft.Radio(value="fulfilled", label="Fulfilled"),
            ft.Radio(value="in progress", label="In Progress"),
        ]),
        value="all", # Default selection
        on_change=filter_changed
    )

    export_button = ft.ElevatedButton(
        "Export to CSV",
        icon=ft.icons.DOWNLOAD,
        on_click=export_clicked
    )
    
    # --- Initial data load ---
    update_table("all")

    page.add(
        ft.Column([
            ft.Text("📋 Match History", size=26, weight="bold", color=ft.colors.BLUE_900),
            # --- NEW: Add the new controls to the layout ---
            ft.Row(
                [
                    ft.Text("Filter by Status:", weight="bold"),
                    status_filter_radios,
                    export_button
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
            ),
            ft.Divider(),
            table
        ])
    )

ft.app(target=main)