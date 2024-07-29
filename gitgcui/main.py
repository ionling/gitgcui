import logging

import flet as ft
import structlog

import git

structlog.configure(
    wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
)


class Repo(ft.Container):
    def __init__(self, path):
        super().__init__()
        self.path = path
        self.dlg = ft.AlertDialog()
        self.files_count = 0
        self.files_count_view = ft.Text()

        self.on_hover = self.handle_on_hover
        self.content = ft.Row(
            [
                ft.Row(
                    [
                        ft.Checkbox(
                            value=git.root(self.path) != "",
                            tooltip="Is Git",
                            disabled=True,
                        ),
                        ft.Text(self.path),
                    ]
                ),
                ft.Row(
                    [
                        self.files_count_view,
                        ft.IconButton(
                            ft.icons.COMPOST,
                            tooltip="GC",
                            on_click=lambda _: self.gc(),
                        ),
                        ft.IconButton(
                            ft.icons.APPS,
                            tooltip="Count files",
                            on_click=lambda _: self.count_files(),
                        ),
                        ft.IconButton(
                            ft.icons.OPEN_IN_NEW_SHARP,
                            tooltip="Open it",
                            on_click=lambda _: self.open(),
                        ),
                    ]
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )

    def handle_on_hover(self, e: ft.ControlEvent):
        e.control.bgcolor = ft.colors.PRIMARY_CONTAINER if e.data == "true" else None
        e.control.update()

    def show_err(self, title, content):
        self.dlg.title = ft.Text(title)
        self.dlg.content = ft.Text(content)
        self.page.open(self.dlg)

    def count_files(self):
        if not self.path:
            self.files_count = 0
            self.files_count_view.value = "no selected repo"
        else:
            self.files_count = git.count_files(self.path)
            self.files_count_view.value = self.files_count
        self.files_count_view.update()

    def gc(self):
        if err := git.gc(self.path):
            self.show_err("Failed to GC", err)
            return

        self.count_files()

    def open(self):
        if err := git.app_open(self.path):
            self.show_err("Failed to open", err)


def main(page: ft.Page):
    page.title = "Git GC UI"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    selected_repo = ft.Text()

    root = "/home"
    repos: list[Repo] = []
    list_view = ft.ListView(repos, height=page.height - 80)
    all_count = ft.Text()

    def update_root(root):
        repos = [Repo(i) for i in git.list_dirs(root)]
        list_view.controls = repos
        list_view.update()

    def sort_repos():
        repos.sort(key=lambda x: x.files_count, reverse=True)
        list_view.update()

    def count_all():
        c = 0
        for repo in repos:
            repo.count_files()
            c += repo.files_count
        all_count.value = c
        all_count.update()

    def handle_pick_repo(e: ft.FilePickerResultEvent):
        root = git.root(e.path)
        if root:
            selected_repo.value = root
        else:
            selected_repo.value = e.path

        root = selected_repo.value
        update_root(root)
        selected_repo.update()

    pick_repo_dialog = ft.FilePicker(on_result=handle_pick_repo)
    page.overlay.append(pick_repo_dialog)
    page.add(
        ft.Row(
            [
                ft.ElevatedButton(
                    "Pick Git repo",
                    icon=ft.icons.COOKIE,
                    on_click=lambda _: pick_repo_dialog.get_directory_path(
                        initial_directory=root
                    ),
                ),
                ft.ElevatedButton(
                    "Count all",
                    icon=ft.icons.ALL_OUT,
                    on_click=lambda _: count_all(),
                ),
                ft.ElevatedButton(
                    "Sort",
                    icon=ft.icons.SORT,
                    on_click=lambda _: sort_repos(),
                ),
            ],
        ),
        ft.Row([ft.Text("Repo path:"), selected_repo]),
        ft.Row([ft.Text("All files:"), all_count]),
        list_view,
    )


ft.app(main)
