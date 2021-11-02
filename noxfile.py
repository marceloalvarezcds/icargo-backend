import nox


@nox.session
def safety(session):
    session.install("poetry")
    session.run("poetry", "install")
    session.run("safety", "check")


@nox.session(python=["3.7", "3.8"])
def tests(session):
    session.install("poetry")
    session.run("poetry", "install")
    session.run("coverage", "run", "-m", "pytest")
    session.run("coverage", "report")


@nox.session
def lint(session):
    session.install("poetry")
    session.run("poetry", "install")
    session.run("black", "--check", ".")
    session.run("isort", "--check-only", ".")
    session.run("flake8", ".")


@nox.session
def typing(session):
    session.install("poetry")
    session.run("poetry", "install")
    session.run("mypy", ".")
