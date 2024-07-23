import flet as ft

import git


def main(page: ft.Page):
    page.title = "Flet counter example"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    selected_repo = ft.Text()
    is_git = ft.Checkbox(label="Is Git repo")
    files_count = ft.TextField(label="Files count", read_only=True)

    def count_files(e):
        if not selected_repo.value:
            files_count.value = "no selected repo"
        else:
            files_count.value = git.count_files(selected_repo.value)
        files_count.update()

    def handle_pick_repo(e: ft.FilePickerResultEvent):
        root = git.root(e.path)
        if root:
            is_git.value = True
            selected_repo.value = root
        else:
            is_git.value = False
            selected_repo.value = e.path

        is_git.update()
        selected_repo.update()
        files_count.value = ""
        files_count.update()

    pick_repo_dialog = ft.FilePicker(on_result=handle_pick_repo)
    page.overlay.append(pick_repo_dialog)
    page.add(
        ft.Row(
            [
                ft.ElevatedButton(
                    "Pick Git repo",
                    icon=ft.icons.COOKIE,
                    on_click=lambda _: pick_repo_dialog.get_directory_path(
                        initial_directory="/home"
                    ),
                ),
                ft.ElevatedButton(
                    "Count files",
                    icon=ft.icons.FILE_PRESENT,
                    on_click=count_files,
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        ft.Row(
            [is_git, files_count],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        ft.Row(
            [
                ft.Text("Repo path:"),
                selected_repo,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
    )


ft.app(main)
