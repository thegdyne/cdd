# src/cdd/executors/static_exec.py
"""Static executor: AST analysis without runtime execution."""
from __future__ import annotations

from typing import Any, Dict

from cdd.executors.base import Executor, RunContext, StepResult, StepSpec


class StaticExecutor:
    """
    Static analysis executor.
    
    Does not execute steps - instead populates $.ast for assertions.
    The runner handles the implicit 'analyze' step.
    """

    name = "static"

    def supports(self, action: str) -> bool:
        # Static executor does not support any runtime actions
        return False

    def setup(self, ctx: RunContext, runner_cfg: Dict[str, Any]) -> None:
        pass

    def execute_step(
        self,
        ctx: RunContext,
        runner_cfg: Dict[str, Any],
        test_id: str,
        step: StepSpec,
        timeout_ms: int,
    ) -> StepResult:
        # Static executor should never be called for steps
        return StepResult(
            ok=False,
            error_code="static_no_steps",
            message="Static executor does not execute steps; use assertions against $.ast",
        )

    def teardown(self, ctx: RunContext, runner_cfg: Dict[str, Any]) -> None:
        pass

    def analyze(self, ctx: RunContext, runner_cfg: Dict[str, Any], source_path: str) -> Dict[str, Any]:
        """
        Analyze source file and return AST blob.
        
        MVP: Returns empty structure. Full implementation requires parser
        specified by runner.parser (sclang_ast, python_ast).
        """
        parser = runner_cfg.get("parser")
        
        # MVP placeholder
        return {
            "schema_version": "1.0",
            "calls": [],
            "bus_reads": {},
            "imports": [],
            "definitions": [],
            "parse_errors": [],
            "parser": parser,
            "source_included": False,
        }
