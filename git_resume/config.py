from typing import List, Optional
import os
import yaml
from pydantic import BaseModel, Field

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

def load_config(config_path: str = "gitresume.yaml") -> GitResumeConfig:
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Configuration file not found: {config_path}")
    with open(config_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return GitResumeConfig(**data)
