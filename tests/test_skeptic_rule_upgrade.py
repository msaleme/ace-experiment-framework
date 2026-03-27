from agents.skeptic.skeptic_agent import SkepticAgent
from src.model import ExperimentRecord


def test_uncertainty_normalized_skeptic_rule_triggers_and_reports_debug():
    agent = SkepticAgent()
    exp = ExperimentRecord(
        experiment_id="exp_002_token_pruning",
        benchmark_set=[
            "transformer_inference_small",
            "transformer_inference_medium",
            "transformer_inference_holdout",
        ],
    )
    summary = {
        "ecd_improvement": {"mean": 1.0, "std": 0.50},
        "ecd_improvement_uncertainty": {"mean": 0.10},
    }

    out = agent.review(exp, summary)
    assert out["suspicious"] is True
    assert out["rule_debug"]["old_rule_triggered"] is True
    assert out["rule_debug"]["new_rule_triggered"] is True
    assert out["rule_debug"]["instability_score"] > 0.35