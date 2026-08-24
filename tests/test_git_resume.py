import os
import pytest
from git_resume.config import load_config
from git_resume.agents.inspector import InspectorAgent
from git_resume.agents.verifier import GroundingVerifierAgent
from git_resume.agents.synthesizer import SynthesizerAgent

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
    ground_truth = {'commits': 400, 'loc': 130000, 'stack': ['Python', 'FastAPI']}
    assert verifier.verify_metrics({'commits': 350}, ground_truth) is True
    assert verifier.verify_metrics({'commits': 450}, ground_truth) is False

def test_synthesizer_agent():
    synthesizer = SynthesizerAgent()
    bullet = synthesizer.synthesize_fundersai({'loc_k': '145K', 'files': 760, 'commits': 402, 'test_suites': 120})
    assert '145K lines of code' in bullet
    assert 'OpenAI Build Week' in bullet