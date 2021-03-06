"""Functions for using git."""
from typing import Optional, Union

from pathlib import Path

from git import InvalidGitRepositoryError, NoSuchPathError, Repo

from cookie_composer.exceptions import GitError


def get_repo(project_dir: Union[str, Path], search_parent_directories: bool = False) -> Repo:
    """
    Get the git Repo object for a directory.

    Args:
        project_dir: The directory containing the .git folder
        search_parent_directories: if ``True``, all parent directories will be searched for a valid repo as well.

    Raises:
        GitError: If the directory is not a git repo

    Returns:
        The GitPython Repo object
    """
    try:
        return Repo(str(project_dir), search_parent_directories=search_parent_directories)
    except (InvalidGitRepositoryError, NoSuchPathError) as e:
        raise GitError(
            "Some cookie composer commands only work on git repositories. "
            "Please make the destination directory a git repo."
        ) from e


def branch_exists(repo: Repo, branch_name: str) -> bool:
    """
    Does the branch exist in the repo?

    Args:
        repo: The repository to check
        branch_name: The name of the branch to check for

    Returns:
        ``True`` if the branch exists
    """
    return branch_name in repo.refs


def remote_branch_exists(repo: Repo, branch_name: str, remote_name: str = "origin") -> bool:
    """
    Does the branch exist in the remote repo?

    Args:
        repo: The repository to check
        branch_name: The name of the branch to check for
        remote_name: The name of the remote reference. Defaults to ``origin``

    Returns:
        ``True`` if the branch exists in the remote repository
    """
    if remote_name in repo.remotes:
        return branch_name in repo.remotes[remote_name].refs

    return False


def checkout_branch(repo: Repo, branch_name: str, remote_name: str = "origin"):
    """Checkout a local or remote branch."""
    if repo.is_dirty():
        raise GitError(
            "Cookie composer cannot apply updates on an unclean git project."
            " Please make sure your git working tree is clean before proceeding."
        )
    if len(repo.remotes) > 0:
        repo.remotes[0].fetch()
    if branch_exists(repo, branch_name):
        repo.heads[branch_name].checkout()
    elif remote_branch_exists(repo, branch_name, remote_name):
        repo.create_head(branch_name, f"origin/{branch_name}")
        repo.heads[branch_name].checkout()

    repo.create_head(branch_name)
    repo.heads[branch_name].checkout()


def branch_from_first_commit(repo: Repo, branch_name: str):
    """Create and checkout a branch from the repo's first commit."""
    if repo.is_dirty():
        raise GitError(
            "Cookie composer cannot apply updates on an unclean git project."
            " Please make sure your git working tree is clean before proceeding."
        )
    first_commit = list(repo.iter_commits("HEAD", max_parents=0, max_count=1))[0]
    repo.create_head(branch_name, first_commit.hexsha)
    repo.heads[branch_name].checkout()


def get_latest_template_commit(template_path: str) -> Optional[str]:
    """
    Get the hexsha of the latest commit on the template path.

    If the path is not a git repository, it returns ``None``.

    Args:
        template_path: The path to the potentially-cloned template

    Returns:
        The hexsha of the latest commit or ``None``
    """
    try:
        repo = get_repo(template_path, search_parent_directories=True)
        return repo.head.commit.hexsha
    except GitError:
        return None
