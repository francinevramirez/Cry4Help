# Display Skill

import flet as ft

def main(page: ft.Page):
    page.title = "Volunteer Skill Display"
    page.window_width = 400
    page.window_height = 500
    page.vertical_alignment = "center"
    page.horizontal_alignment = "center"

    skills = ft.TextField(label="List Your Skills (comma-separated)", width=350)
    status = ft.Text("")
    skill_list = ft.Column([])

    def submit_skills(e):
        entered_skills = [s.strip() for s in skills.value.split(",") if s.strip()]
        skill_list.controls.clear()
        if entered_skills:
            for skill in entered_skills:
                skill_list.controls.append(ft.Text(f"- {skill}"))
            status.value = "Skills displayed below."
            status.color = "green"
        else:
            status.value = "Please enter at least one skill."
            status.color = "red"
        page.update()

    page.add(
        ft.Column([
            ft.Text("Volunteer Skill Manager", size=20, weight="bold"),
            skills,
            ft.ElevatedButton("Show Skills", on_click=submit_skills),
            status,
            ft.Text("Your Skills:", size=16, weight="bold"),
            skill_list,
        ], alignment="center", horizontal_alignment="center")
    )

if __name__ == "__main__":
    ft.app(target=main)

