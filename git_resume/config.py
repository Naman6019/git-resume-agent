from typing import List, Optional
import os
import yaml
from pydantic import BaseModel, Field

import subprocess
from git_resume.utils.git_utils import get_git_config

class DeveloperConfig(BaseModel):
    name: str
    email: str
    github: str
    linkedin: Optional[str] = None
    location: Optional[str] = None

class LLMConfig(BaseModel):
    provider: str = "ollama"
    model: str = "qwen2.5-coder:7b"
    fallback_model: str = "gpt-4o-mini"
    temperature: float = 0.2
    api_key_env: str = "OPENAI_API_KEY"

class RepoConfig(BaseModel):
    name: str
    path: str
    tag: Optional[str] = None
    primary_stack: List[str] = Field(default_factory=list)
    repo_url: Optional[str] = None
    live_url: Optional[str] = None
    deployed: Optional[bool] = None

    @property
    def is_deployed(self) -> bool:
        if self.deployed is not None:
            return self.deployed
        return bool(self.live_url)

    @property
    def formatted_links(self) -> str:
        """Returns both live link and repo link if deployed, otherwise repo link."""
        parts = []
        if self.is_deployed and self.live_url:
            parts.append(f"Live: {self.live_url}")
        if self.repo_url:
            parts.append(f"Repo: {self.repo_url}")
        return " | ".join(parts) if parts else ""

class PersonaConfig(BaseModel):
    id: str
    title: str
    resume_file: str
    emphasis: List[str] = Field(default_factory=list)

class OutputConfig(BaseModel):
    formats: List[str] = Field(default_factory=lambda: ["docx", "pdf"])
    resume_dir: str
    sync_paths: List[str] = Field(default_factory=list)

class GitResumeConfig(BaseModel):
    version: str = "1.0"
    developer: DeveloperConfig
    llm: LLMConfig = Field(default_factory=LLMConfig)
    repositories: List[RepoConfig] = Field(default_factory=list)
    personas: List[PersonaConfig] = Field(default_factory=list)
    output: OutputConfig

def find_config_path(config_path: Optional[str] = "gitresume.yaml") -> str:
    """
    Resolves the master gitresume.yaml configuration using multi-layered fallback hierarchy:
    1. Direct path check if explicitly given and exists.
    2. Environment variable: GITRESUME_CONFIG
    3. Git repository config: git config --get gitresume.config (current working directory)
    4. Upward traversal from current working directory for gitresume.yaml or .gitresume.yaml
    5. Global Git config: git config --global --get gitresume.config
    6. User home config: ~/.config/git-resume/gitresume.yaml or ~/.gitresume.yaml
    """
    # 1. Direct explicit path check (if non-default or if default file exists in cwd)
    if config_path and os.path.exists(config_path):
        return os.path.abspath(config_path)

    # 2. Environment variable
    env_path = os.environ.get("GITRESUME_CONFIG")
    if env_path and os.path.exists(env_path):
        return os.path.abspath(env_path)

    # 3. Local Git repository config (git config --get gitresume.config)
    local_git_config = get_git_config("gitresume.config")
    if local_git_config and os.path.exists(local_git_config):
        return os.path.abspath(local_git_config)

    # 4. Upward directory search starting from os.getcwd()
    try:
        current = os.path.abspath(os.getcwd())
        while True:
            for fname in ["gitresume.yaml", ".gitresume.yaml"]:
                candidate = os.path.join(current, fname)
                if os.path.exists(candidate):
                    return candidate
            parent = os.path.dirname(current)
            if parent == current:
                break
            current = parent
    except Exception:
        pass

    # 5. Global Git config (git config --global --get gitresume.config)
    try:
        global_cmd = ["git", "config", "--global", "--get", "gitresume.config"]
        global_cfg = subprocess.check_output(global_cmd, text=True, stderr=subprocess.DEVNULL).strip()
        if global_cfg and os.path.exists(global_cfg):
            return os.path.abspath(global_cfg)
    except Exception:
        pass

    # 6. User home directory
    home = os.path.expanduser("~")
    for candidate in [
        os.path.join(home, ".config", "git-resume", "gitresume.yaml"),
        os.path.join(home, ".gitresume.yaml"),
        os.path.join(home, "gitresume.yaml"),
    ]:
        if os.path.exists(candidate):
            return candidate

    target = config_path or "gitresume.yaml"
    raise FileNotFoundError(
        f"Configuration file not found: '{target}'.\n"
        f"Searched in: current working directory, GITRESUME_CONFIG environment variable, "
        f"git config 'gitresume.config', parent directories, and user home directory.\n"
        f"Run 'git-resume auto-config' or specify --config-path / set GITRESUME_CONFIG."
    )

def load_config(config_path: str = "gitresume.yaml") -> GitResumeConfig:
    resolved_path = find_config_path(config_path)
    with open(resolved_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return GitResumeConfig(**data)

