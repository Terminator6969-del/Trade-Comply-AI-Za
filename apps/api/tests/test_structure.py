"""
Test suite for monorepo structure validation.
Tests that all required files and directories exist.
"""

import os
from pathlib import Path


def get_workspace_root() -> Path:
    """Get the workspace root directory."""
    return Path(__file__).parent.parent.parent.parent


def test_monorepo_structure():
    """Test that monorepo directory structure exists."""
    root = get_workspace_root()

    # Required directories
    required_dirs = [
        "apps/api",
        "apps/api/app",
        "apps/api/app/core",
        "apps/api/app/models",
        "apps/api/app/schemas",
        "apps/api/app/routers",
        "apps/api/app/services",
        "apps/api/app/ai",
        "apps/api/app/rules",
        "apps/api/app/workers",
        "apps/api/tests",
        "apps/api/alembic",
        "apps/api/alembic/versions",
        "apps/web",
        "apps/web/app",
        "apps/web/components",
        "apps/web/lib",
        "apps/web/public",
        "packages/shared-types",
        "packages/shared-types/src",
        "infra",
        "scripts",
        "docs",
    ]

    for dir_path in required_dirs:
        full_path = root / dir_path
        assert full_path.exists(), f"Directory not found: {dir_path}"
        assert full_path.is_dir(), f"Path is not a directory: {dir_path}"


def test_pyproject_toml_exists():
    """Test that pyproject.toml exists for backend."""
    root = get_workspace_root()
    pyproject = root / "apps/api/pyproject.toml"
    assert pyproject.exists(), "pyproject.toml not found in apps/api"
    assert pyproject.is_file(), "pyproject.toml is not a file"


def test_package_json_exists():
    """Test that package.json exists for frontend."""
    root = get_workspace_root()
    package_json = root / "apps/web/package.json"
    assert package_json.exists(), "package.json not found in apps/web"
    assert package_json.is_file(), "package.json is not a file"


def test_docker_compose_exists():
    """Test that docker-compose.yml exists."""
    root = get_workspace_root()
    docker_compose = root / "infra/docker-compose.yml"
    assert docker_compose.exists(), "docker-compose.yml not found in infra"
    assert docker_compose.is_file(), "docker-compose.yml is not a file"


def test_makefile_exists():
    """Test that Makefile exists."""
    root = get_workspace_root()
    makefile = root / "Makefile"
    assert makefile.exists(), "Makefile not found in workspace root"
    assert makefile.is_file(), "Makefile is not a file"


def test_readme_exists():
    """Test that README.md exists."""
    root = get_workspace_root()
    readme = root / "README.md"
    assert readme.exists(), "README.md not found in workspace root"
    assert readme.is_file(), "README.md is not a file"


def test_gitignore_exists():
    """Test that .gitignore exists."""
    root = get_workspace_root()
    gitignore = root / ".gitignore"
    assert gitignore.exists(), ".gitignore not found in workspace root"
    assert gitignore.is_file(), ".gitignore is not a file"


def test_env_example_exists():
    """Test that .env.example exists."""
    root = get_workspace_root()
    env_example = root / "infra/.env.example"
    assert env_example.exists(), ".env.example not found in infra"
    assert env_example.is_file(), ".env.example is not a file"


def test_shared_types_index_exists():
    """Test that shared types index exists."""
    root = get_workspace_root()
    index = root / "packages/shared-types/src/index.ts"
    assert index.exists(), "index.ts not found in packages/shared-types/src"
    assert index.is_file(), "index.ts is not a file"


def test_dockerfiles_exist():
    """Test that all Dockerfiles exist."""
    root = get_workspace_root()
    dockerfiles = [
        "apps/api/Dockerfile",
        "apps/api/Dockerfile.worker",
        "apps/web/Dockerfile",
    ]

    for dockerfile_path in dockerfiles:
        full_path = root / dockerfile_path
        assert full_path.exists(), f"Dockerfile not found: {dockerfile_path}"
        assert full_path.is_file(), f"Dockerfile is not a file: {dockerfile_path}"


if __name__ == "__main__":
    test_monorepo_structure()
    test_pyproject_toml_exists()
    test_package_json_exists()
    test_docker_compose_exists()
    test_makefile_exists()
    test_readme_exists()
    test_gitignore_exists()
    test_env_example_exists()
    test_shared_types_index_exists()
    test_dockerfiles_exist()

    print("✅ All monorepo structure tests passed!")
