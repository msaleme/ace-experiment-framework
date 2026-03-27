def test_core_modules_importable():
    import src.baseline_manager  # noqa: F401
    import src.benchmark_registry  # noqa: F401
    import src.metrics_collector  # noqa: F401
    import src.experiment_runner  # noqa: F401
    import src.stats_evaluator  # noqa: F401
    import src.results_store  # noqa: F401
    import src.report_generator  # noqa: F401


def test_full_runner_importable():
    import run_full_program  # noqa: F401
