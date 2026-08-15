def test_core_modules_importable():
    import ace_lab.baseline_manager  # noqa: F401
    import ace_lab.benchmark_registry  # noqa: F401
    import ace_lab.metrics_collector  # noqa: F401
    import ace_lab.experiment_runner  # noqa: F401
    import ace_lab.stats_evaluator  # noqa: F401
    import ace_lab.results_store  # noqa: F401
    import ace_lab.report_generator  # noqa: F401


def test_full_runner_importable():
    import run_full_program  # noqa: F401
