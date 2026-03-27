"""
Stats Evaluator: statistical analysis and verdict generation.
Computes confidence intervals, effect sizes, and significance tests.
"""
from typing import Dict, Optional, Tuple, Any
import statistics
import math
from scipy import stats
from src.metrics_collector import MetricsCollector
from src.model import ExperimentRecord, Verdict


class StatsEvaluator:
    """
    Statistical analysis for experiments.
    
    Responsibilities:
    1. Compute effect size
    2. Calculate confidence intervals
    3. Perform significance tests (Welch's t-test, etc.)
    4. Check variance and outliers
    5. Emit statistical verdict
    
    Design:
    - Never accept based on single run
    - Require effect size, not just p-values
    - Bootstrap confidence intervals for unstable metrics
    - Detect and handle outliers per policy
    """
    
    # Configuration constants
    DEFAULT_CONFIDENCE_LEVEL = 0.95
    OUTLIER_DETECTION_METHOD = "tukey_fences"  # tukey_fences, zscore
    ZSCORE_THRESHOLD = 3.0
    
    def __init__(self, metrics_collector: MetricsCollector):
        """Initialize stats evaluator."""
        self.metrics_collector = metrics_collector
    
    def compute_effect_size(
        self,
        candidate_values: list,
        baseline_values: list,
    ) -> float:
        """
        Compute Cohen's d effect size.
        
        Args:
            candidate_values: Metric values from candidate
            baseline_values: Metric values from baseline
            
        Returns:
            Cohen's d effect size
        """
        if not candidate_values or not baseline_values:
            return 0.0
        
        mean_candidate = statistics.mean(candidate_values)
        mean_baseline = statistics.mean(baseline_values)
        
        if len(candidate_values) == 1 or len(baseline_values) == 1:
            # Can't compute std dev with 1 sample
            return abs(mean_candidate - mean_baseline)
        
        std_candidate = statistics.stdev(candidate_values)
        std_baseline = statistics.stdev(baseline_values)
        
        # Pooled standard deviation
        n1, n2 = len(candidate_values), len(baseline_values)
        pooled_std = math.sqrt(
            ((n1 - 1) * std_candidate**2 + (n2 - 1) * std_baseline**2) / (n1 + n2 - 2)
        )
        
        if pooled_std == 0:
            return 0.0
        
        cohens_d = (mean_candidate - mean_baseline) / pooled_std
        return cohens_d
    
    def compute_confidence_interval(
        self,
        values: list,
        confidence_level: float = DEFAULT_CONFIDENCE_LEVEL,
        method: str = "bootstrap",
    ) -> Tuple[float, float]:
        """
        Compute confidence interval for a metric.
        
        Args:
            values: List of metric values
            confidence_level: Confidence level (default 0.95 = 95%)
            method: "bootstrap" or "ttest"
            
        Returns:
            Tuple of (lower, upper) bounds
        """
        if not values or len(values) < 2:
            return (0.0, 0.0)
        
        if method == "bootstrap":
            return self._bootstrap_ci(values, confidence_level)
        elif method == "ttest":
            return self._ttest_ci(values, confidence_level)
        else:
            raise ValueError(f"Unknown CI method: {method}")
    
    def perform_welch_ttest(
        self,
        candidate_values: list,
        baseline_values: list,
        two_tailed: bool = True,
    ) -> Dict[str, float]:
        """
        Perform Welch's t-test (doesn't assume equal variances).
        
        Args:
            candidate_values: Candidate metric values
            baseline_values: Baseline metric values
            two_tailed: If True, two-tailed test; if False, one-tailed
            
        Returns:
            Dictionary with t_statistic, p_value, significant (at 0.05)
        """
        if len(candidate_values) < 2 or len(baseline_values) < 2:
            return {
                't_statistic': 0.0,
                'p_value': 1.0,
                'significant': False,
            }
        
        # Welch's t-test
        t_stat, p_value = stats.ttest_ind(
            candidate_values,
            baseline_values,
            equal_var=False,
        )
        
        # For one-tailed, divide p by 2 if in expected direction
        if not two_tailed:
            mean_cand = statistics.mean(candidate_values)
            mean_base = statistics.mean(baseline_values)
            if (t_stat > 0 and mean_cand < mean_base) or (t_stat < 0 and mean_cand > mean_base):
                p_value = 1.0 - p_value / 2
            else:
                p_value = p_value / 2
        
        return {
            't_statistic': float(t_stat),
            'p_value': float(p_value),
            'significant': p_value < 0.05,
        }
    
    def detect_outliers(
        self,
        values: list,
        method: str = "tukey_fences",
    ) -> Tuple[list, list]:
        """
        Detect outliers in values.
        
        Args:
            values: List of values
            method: "tukey_fences" or "zscore"
            
        Returns:
            Tuple of (clean_values, outlier_values)
        """
        if not values or len(values) < 4:
            return (values, [])
        
        if method == "tukey_fences":
            return self._tukey_outliers(values)
        elif method == "zscore":
            return self._zscore_outliers(values)
        else:
            raise ValueError(f"Unknown outlier detection method: {method}")
    
    def check_quality_floor(
        self,
        candidate_quality_values: list,
        baseline_quality_mean: float,
        quality_floor: float = 0.99,
    ) -> bool:
        """
        Check if candidate meets quality floor.
        
        Args:
            candidate_quality_values: Quality values from candidate
            baseline_quality_mean: Mean quality of baseline
            quality_floor: Minimum acceptable relative to baseline
            
        Returns:
            True if quality floor is met
        """
        if not candidate_quality_values:
            return False
        
        candidate_mean = statistics.mean(candidate_quality_values)
        
        # Quality floor is relative: candidate_mean >= baseline_mean * quality_floor
        return candidate_mean >= baseline_quality_mean * quality_floor
    
    def check_latency_budget(
        self,
        candidate_p95_latency: float,
        latency_budget_ms_p95: float,
    ) -> bool:
        """
        Check if candidate meets latency budget.
        
        Args:
            candidate_p95_latency: p95 latency in ms
            latency_budget_ms_p95: Budget in ms
            
        Returns:
            True if within budget
        """
        return candidate_p95_latency <= latency_budget_ms_p95
    
    def generate_verdict(
        self,
        experiment: ExperimentRecord,
        baseline_metrics: Dict[str, list],
        candidate_metrics: Dict[str, list],
    ) -> Dict[str, Any]:
        """
        Generate statistical verdict for experiment.
        
        Args:
            experiment: ExperimentRecord with evaluation_config
            baseline_metrics: Dict[metric_name, values] from baseline
            candidate_metrics: Dict[metric_name, values] from candidate
            
        Returns:
            Dictionary with verdict and supporting statistics
        """
        config = experiment.evaluation_config
        results = {
            'quality_floor_met': False,
            'latency_budget_met': False,
            'minimum_effect_met': False,
            'statistically_significant': False,
            'confidence_interval_excludes_zero': False,
            'overall_verdict': Verdict.PENDING,
            'reasoning': [],
            'metrics_analysis': {},
        }
        
        # Primary metric for ECD improvement (assume first primary metric from benchmark)
        primary_metric = experiment.benchmark_set[0] if experiment.benchmark_set else "throughput"
        primary_key = f"{primary_metric}_ecd_improvement"
        
        if primary_key not in candidate_metrics:
            results['reasoning'].append("No primary metric data available")
            results['overall_verdict'] = Verdict.INCONCLUSIVE
            return results
        
        candidate_values = candidate_metrics.get(primary_key, [])
        baseline_values = baseline_metrics.get(primary_key, [])
        
        if not candidate_values or not baseline_values:
            results['reasoning'].append("Insufficient data for comparison")
            results['overall_verdict'] = Verdict.INCONCLUSIVE
            return results
        
        # Compute statistics
        effect_size = self.compute_effect_size(candidate_values, baseline_values)
        ci_lower, ci_upper = self.compute_confidence_interval(candidate_values)
        ttest = self.perform_welch_ttest(candidate_values, baseline_values)
        
        results['metrics_analysis'][primary_key] = {
            'effect_size': effect_size,
            'confidence_interval': (ci_lower, ci_upper),
            'welch_ttest': ttest,
            'baseline_mean': statistics.mean(baseline_values),
            'candidate_mean': statistics.mean(candidate_values),
        }
        
        # Check conditions
        effect_met = abs(effect_size) >= config.minimum_effect_threshold
        results['minimum_effect_met'] = effect_met
        if effect_met:
            results['reasoning'].append(f"Minimum effect threshold met: {effect_size:.3f}")
        else:
            results['reasoning'].append(
                f"Effect size {effect_size:.3f} below threshold {config.minimum_effect_threshold}"
            )
        
        # Check CI excludes zero (confidence interval should not cross baseline)
        ci_excludes_zero = (ci_lower > 0) or (ci_upper < 0)
        results['confidence_interval_excludes_zero'] = ci_excludes_zero
        if ci_excludes_zero:
            results['reasoning'].append(f"CI [{ci_lower:.3f}, {ci_upper:.3f}] excludes zero")
        else:
            results['reasoning'].append(f"CI [{ci_lower:.3f}, {ci_upper:.3f}] includes zero")
        
        # Check statistical significance
        sig = ttest['significant']
        results['statistically_significant'] = sig
        if sig:
            results['reasoning'].append(f"Significant at p=0.05 (p={ttest['p_value']:.4f})")
        else:
            results['reasoning'].append(f"Not significant at p=0.05 (p={ttest['p_value']:.4f})")
        
        # Determine verdict
        all_conditions_met = (
            effect_met and
            config.confidence_interval_excludes_zero and ci_excludes_zero and
            sig
        )
        
        if all_conditions_met:
            results['overall_verdict'] = Verdict.ACCEPTED
            results['reasoning'].append("All acceptance criteria met")
        else:
            results['overall_verdict'] = Verdict.REJECTED
            results['reasoning'].append("One or more acceptance criteria not met")
        
        return results
    
    def _bootstrap_ci(
        self,
        values: list,
        confidence_level: float,
        n_bootstrap: int = 1000,
    ) -> Tuple[float, float]:
        """Compute bootstrap confidence interval."""
        import numpy as np
        
        if len(values) < 2:
            return (min(values), max(values)) if values else (0.0, 0.0)
        
        bootstrap_means = []
        values_array = np.array(values)
        
        for _ in range(n_bootstrap):
            bootstrap_sample = np.random.choice(values_array, size=len(values), replace=True)
            bootstrap_means.append(np.mean(bootstrap_sample))
        
        alpha = 1 - confidence_level
        lower_percentile = (alpha / 2) * 100
        upper_percentile = (1 - alpha / 2) * 100
        
        lower = np.percentile(bootstrap_means, lower_percentile)
        upper = np.percentile(bootstrap_means, upper_percentile)
        
        return (float(lower), float(upper))
    
    def _ttest_ci(
        self,
        values: list,
        confidence_level: float,
    ) -> Tuple[float, float]:
        """Compute t-test-based confidence interval."""
        if len(values) < 2:
            return (min(values), max(values)) if values else (0.0, 0.0)
        
        mean = statistics.mean(values)
        std = statistics.stdev(values)
        n = len(values)
        
        # t-critical value
        alpha = 1 - confidence_level
        t_crit = stats.t.ppf(1 - alpha / 2, n - 1)
        
        margin = t_crit * (std / math.sqrt(n))
        
        return (mean - margin, mean + margin)
    
    def _tukey_outliers(self, values: list) -> Tuple[list, list]:
        """Detect outliers using Tukey fences (Q1 - 1.5*IQR, Q3 + 1.5*IQR)."""
        sorted_values = sorted(values)
        n = len(sorted_values)
        
        q1_idx = n // 4
        q3_idx = (3 * n) // 4
        
        q1 = sorted_values[q1_idx]
        q3 = sorted_values[q3_idx]
        iqr = q3 - q1
        
        lower_fence = q1 - 1.5 * iqr
        upper_fence = q3 + 1.5 * iqr
        
        clean = [v for v in values if lower_fence <= v <= upper_fence]
        outliers = [v for v in values if v < lower_fence or v > upper_fence]
        
        return (clean, outliers)
    
    def _zscore_outliers(self, values: list) -> Tuple[list, list]:
        """Detect outliers using z-score threshold."""
        if not values:
            return ([], [])
        
        mean = statistics.mean(values)
        if len(values) > 1:
            std = statistics.stdev(values)
        else:
            std = 0.0
        
        if std == 0:
            return (values, [])
        
        clean = []
        outliers = []
        
        for v in values:
            z_score = abs((v - mean) / std)
            if z_score <= self.ZSCORE_THRESHOLD:
                clean.append(v)
            else:
                outliers.append(v)
        
        return (clean, outliers)
