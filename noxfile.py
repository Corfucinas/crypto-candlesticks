# -*- coding: utf-8 -*-
"""All Nox sessions."""

# built-in
import tempfile

# external
import nox
from nox.sessions import Session


nox.options.sessions = ('black', 'lint', 'safety', 'mypy', 'tests', 'docs')


locations = ('./src', './tests', './noxfile.py', './docs/conf.py')


def install_with_constraints(
    session: Session, *args: str, **kwargs: list[str]
) -> None:
    """Install packages constrained by Poetry's lock file.

    This function is a wrapper for nox.sessions.Session.install. It
    invokes pip to install packages inside of the session's virtualenv.
    Additionally, pip is passed a constraints file generated from
    Poetry's lock file, to ensure that the packages are pinned to the
    versions specified in poetry.lock. This allows you to manage the
    packages as Poetry development dependencies.

    Arguments:
        session: The Session object.
        args: Command-line arguments for pip.
        kwargs: Additional keyword arguments for Session.install.

    """
    with tempfile.NamedTemporaryFile(delete=False) as requirements:
        session.run(
            'poetry',
            'export',
            '--dev',
            '--without-hashes',
            '--format=requirements.txt',
            f'--output={requirements.name}',
            external=True,
        )
        session.install(f'--constraint={requirements.name}', *args, **kwargs)


@nox.session(reuse_venv=True)
def black(session: Session) -> None:
    """Run black code formatter.

    Args:
        session (Session): Session passed by Nox
    """
    args = session.posargs or locations
    install_with_constraints(session, 'black')
    session.run('black', *args)


@nox.session(reuse_venv=True)
def lint(session: Session) -> None:
    """Lint using flake8.

    Args:
        session (Session): Session passed by Nox
    """
    args = session.posargs or locations
    install_with_constraints(
        session, 'flakeheaven', 'pre-commit', 'wemake-python-styleguide'
    )
    session.run('pre-commit', 'run', '--all-files', '--show-diff-on-failure')
    session.run('flakeheaven', 'lint', *args)


@nox.session(reuse_venv=True)
def safety(session: Session) -> None:
    """Scan dependencies for insecure packages.

    Args:
        session (Session): Session passed by Nox
    """
    with tempfile.NamedTemporaryFile(delete=False) as requirements:
        session.run(
            'poetry',
            'export',
            '--dev',
            '--format=requirements.txt',
            '--without-hashes',
            f'--output={requirements.name}',
            external=True,
        )
        install_with_constraints(session, 'safety')
        session.run(
            'safety', 'check', f'--file={requirements.name}', '--full-report'
        )


@nox.session(reuse_venv=True)
def mypy(session: Session) -> None:
    """Type-check using mypy.

    Args:
        session (Session): Session passed by Nox
    """
    args = session.posargs or locations
    install_with_constraints(session, 'mypy')
    session.run('mypy', '--ignore-missing-imports', *args)


@nox.session(reuse_venv=True)
def tests(session: Session) -> None:
    """Run the test suite.

    Args:
        session (Session): Session passed by Nox
    """
    args = session.posargs or ['--cov']
    session.run('poetry', 'install', '--no-dev', external=True)
    install_with_constraints(
        session, 'coverage[toml]', 'pytest', 'pytest-cov', 'pytest-mock'
    )
    session.run('pytest', '-s', '--durations=0', *args)


@nox.session(reuse_venv=True)
def xdoctest(session: Session) -> None:
    """Run examples with xdoctest.

    Args:
        session (Session): Session passed by Nox
    """
    args = session.posargs or ['all']
    session.run('poetry', 'install', '--no-dev', external=True)
    install_with_constraints(session, 'xdoctest')
    session.run('xdoctest', 'crypto_candlesticks', *args)


@nox.session(reuse_venv=True)
def coverage(session: Session) -> None:
    """Upload the coverage data.

    Args:
        session (Session):  Session passed by Nox
    """
    session.run('poetry', 'install', external=True)
    session.run('coverage', 'xml', '--fail-under=0')
    session.run('codecov', *session.posargs)


@nox.session(reuse_venv=True)
def docs(session: Session) -> None:
    """Build the Sphinx documentation.

    Args:
        session (Session): Session passed by Nox
    """
    session.run('poetry', 'install', '--no-dev', external=True)
    install_with_constraints(
        session,
        'toml',
        'sphinx',
        'furo',
        'sphinx-copybutton',
        'sphinxext-opengraph',
    )
    session.run(
        'sphinx-apidoc',
        '-f',
        '-o',
        './docs/',
        './src/crypto_candlesticks/',
    )
    session.run('sphinx-autogen', '-a', '-o', './docs/', './docs/index.rst')
    session.run('sphinx-build', '-v', './docs', './docs/_build/html')
