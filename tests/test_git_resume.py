import os
import pytest
from git_resume.config import load_config
from git_resume.agents.inspector import InspectorAgent
from git_resume.agents.verifier import GroundingVerifierAgent
from git_resume.agents.synthesizer import SynthesizerAgent
from git_resume.agents.schema_discoverer import SchemaDiscoverer

def test_load_config():
    config = load_config('gitresume.yaml')
    assert config.developer.name == 'Naman Manocha'
    assert len(config.repositories) >= 2
    assert len(config.personas) >= 3

def test_inspector_agent():
    inspector = InspectorAgent()
    config = load_config('gitresume.yaml')
    stats = inspector.inspect_all(config.repositories)
    assert 'FundersAI' in stats
    assert stats['FundersAI']['commits'] > 0
    assert stats['FundersAI']['loc'] > 0

def test_grounding_verifier():
    verifier = GroundingVerifierAgent()
    ground_truth = {'loc_k': '130K', 'stack': ['Python', 'FastAPI']}
    valid, msg = verifier.verify_bullet("Engineered system with 130K lines of code.", ground_truth)
    assert valid is True
    invalid, msg = verifier.verify_bullet("Engineered system with 900K lines of code.", ground_truth)
    assert invalid is False

def test_synthesizer_agent():
    synthesizer = SynthesizerAgent()
    bullet = synthesizer.synthesize_fundersai({'loc_k': '145K', 'files': 760, 'commits': 402, 'test_suites': 120})
    assert '145K lines of code' in bullet
    assert 'OpenAI Build Week' in bullet

def test_schema_discoverer():
    discoverer = SchemaDiscoverer()
    funders_meta = discoverer.discover_repo_metadata(r"C:\Users\naman\OneDrive\Desktop\FundersAI", "FundersAI")
    assert "FastAPI" in funders_meta["primary_stack"]
    assert "React" in funders_meta["primary_stack"] or "Python" in funders_meta["primary_stack"]
    assert funders_meta["tag"] == "OpenAI Build Week Submission"
