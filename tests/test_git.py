from gitgcui import git


def test_exec_not_git():
    res = git.exec(["git", "rev-parse", "--show-toplevel"], cwd="/home")
    assert res.stdout == ""
    assert "fatal: not a git repository" in res.stderr
    assert res.returncode == 128


def test_exec_git():
    res = git.exec(["git", "rev-parse", "--show-toplevel"])
    assert "gitgcui\n" in res.stdout
    assert not res.stderr
    assert res.returncode == 0


def test_gc():
    assert "fatal: not a git repository" in git.gc("/home")
    assert not git.gc(".")


def test_root_file():
    assert "gitgcui" in git.root("README.md")
    assert not git.root("/home")


def test_count_files():
    c = git.count_files(".")
    assert c > 20


def test_list_dirs():
    dirs = git.list_dirs(".")
    assert len(dirs) == 4
    dirs2 = git.list_dirs("/home")
    assert len(dirs2) == 1
