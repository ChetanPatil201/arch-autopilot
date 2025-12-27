from arch_autopilot.graph.evaluator import FindingsEvaluator


def test_evaluator_rejects_added_finding():
    original = [
        {
            "rule_id": "AZ001",
            "resource_type": "azurerm_storage_account",
            "resource_name": "sa",
            "file": "sample_tf/main.tf",
        }
    ]

    modified = original + [
        {
            "rule_id": "FAKE",
            "resource_type": "azurerm_key_vault",
            "resource_name": "kv",
            "file": "sample_tf/main.tf",
        }
    ]

    ev = FindingsEvaluator()
    result = ev.evaluate(original, modified)
    assert not result.passed
