# src/cdd/cli.py
"""CDD command-line interface."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from cdd.coverage import compute_coverage
from cdd.executors.registry import ExecutorRegistry
from cdd.lint import lint_contracts
from cdd.runner import ContractRunner
from cdd.spec import get_tool_version, load_spec_text

console = Console()


def main(argv: Optional[List[str]] = None) -> int:
    """Main CLI entrypoint."""
    parser = argparse.ArgumentParser(prog="cdd", description="Contract-Driven Development tooling")
    sub = parser.add_subparsers(dest="cmd", required=True)

    # cdd spec
    p_spec = sub.add_parser("spec", help="Print the embedded spec/version")
    p_spec.add_argument("--print", dest="do_print", action="store_true", help="Print spec text")
    p_spec.add_argument("--version", action="store_true", help="Print tool/spec version")

    # cdd lint
    p_lint = sub.add_parser("lint", help="Lint contract files (schema + coverage gates)")
    p_lint.add_argument("path", nargs="?", default="contracts", help="Contracts directory or file")
    p_lint.add_argument("--json", action="store_true", help="Emit machine-readable JSON")
    p_lint.add_argument("--strict", action="store_true", help="Treat warnings as errors")

    # cdd test
    p_test = sub.add_parser("test", help="Run contract tests")
    p_test.add_argument("path", nargs="?", default="contracts", help="Contracts directory or file")
    p_test.add_argument("--json", action="store_true", help="Emit machine-readable JSON report")
    p_test.add_argument("--artifacts", default="artifacts", help="Artifacts output root")
    p_test.add_argument("--require-exact-spec", action="store_true", help="Error unless exact spec match")
    p_test.add_argument("--var", action="append", default=[], help="Inject variable (key=value). Repeatable.")
    p_test.add_argument("--matrix-fail-fast", action="store_true", help="Stop on first failing target")
    p_test.add_argument("--only", action="append", default=[], help="Run only matching test ids (repeatable)")

    # cdd coverage
    p_cov = sub.add_parser("coverage", help="Requirement coverage report")
    p_cov.add_argument("path", nargs="?", default="contracts", help="Contracts directory or file")
    p_cov.add_argument("--json", action="store_true", help="Emit machine-readable JSON")
    p_cov.add_argument("--strict", action="store_true", help="Exit non-zero if uncovered requirements exist")

    args = parser.parse_args(argv)

    if args.cmd == "spec":
        return cmd_spec(args)
    if args.cmd == "lint":
        return cmd_lint(args)
    if args.cmd == "test":
        return cmd_test(args)
    if args.cmd == "coverage":
        return cmd_coverage(args)

    parser.print_help()
    return 2


# Console-script entrypoints
def contract_lint() -> None:
    raise SystemExit(main(["lint", *sys.argv[1:]]))


def contract_test() -> None:
    raise SystemExit(main(["test", *sys.argv[1:]]))


def contract_coverage() -> None:
    raise SystemExit(main(["coverage", *sys.argv[1:]]))


def cmd_spec(args: argparse.Namespace) -> int:
    if args.version:
        console.print(get_tool_version())
        return 0
    if args.do_print:
        console.print(load_spec_text())
        return 0
    console.print(get_tool_version())
    return 0


def cmd_lint(args: argparse.Namespace) -> int:
    contracts_path = Path(args.path)
    res = lint_contracts(contracts_path, strict=args.strict)

    if args.json:
        console.print_json(json.dumps(res))
    else:
        _print_lint(res)

    return 0 if res["ok"] else 1


def cmd_coverage(args: argparse.Namespace) -> int:
    contracts_path = Path(args.path)
    cov = compute_coverage(contracts_path)

    if args.json:
        console.print_json(json.dumps(cov))
    else:
        _print_coverage(cov)

    if args.strict and cov["uncovered_count"] > 0:
        return 1
    return 0


def cmd_test(args: argparse.Namespace) -> int:
    contracts_path = Path(args.path)
    artifacts_root = Path(args.artifacts)

    injected_vars = _parse_vars(args.var)

    registry = ExecutorRegistry.discover()
    runner = ContractRunner(
        executors=registry,
        artifacts_root=artifacts_root,
        require_exact_spec=args.require_exact_spec,
        matrix_fail_fast=args.matrix_fail_fast,
    )

    report = runner.run(contracts_path, injected_vars=injected_vars, only_test_ids=args.only or None)

    if args.json:
        console.print_json(json.dumps(report))
    else:
        _print_report(report)

    summary = report.get("summary", {})
    has_failures = summary.get("failed", 0) > 0 or summary.get("error", 0) > 0
    return 1 if has_failures else 0


def _parse_vars(kvs: List[str]) -> Dict[str, Any]:
    out: Dict[str, Any] = {}
    for kv in kvs:
        if "=" not in kv:
            raise SystemExit(f"--var must be key=value, got: {kv}")
        k, v = kv.split("=", 1)
        out[k.strip()] = v
    return out


def _print_lint(res: Dict[str, Any]) -> None:
    status = "[green]PASS[/green]" if res["ok"] else "[red]FAIL[/red]"
    body = Table(show_header=False, box=None)
    body.add_row("Status", status)
    body.add_row("Contracts", str(res.get("contracts_checked", 0)))
    body.add_row("Errors", str(len(res.get("errors", []))))
    body.add_row("Warnings", str(len(res.get("warnings", []))))
    console.print(Panel(body, title="CDD Lint"))

    if res.get("errors"):
        t = Table(title="Errors")
        t.add_column("Code")
        t.add_column("Message")
        for e in res["errors"]:
            t.add_row(e.get("code", ""), e.get("message", ""))
        console.print(t)

    if res.get("warnings"):
        t = Table(title="Warnings")
        t.add_column("Code")
        t.add_column("Message")
        for w in res["warnings"]:
            t.add_row(w.get("code", ""), w.get("message", ""))
        console.print(t)


def _print_coverage(cov: Dict[str, Any]) -> None:
    t = Table(title="CDD Coverage")
    t.add_column("Requirement")
    t.add_column("Linked tests", justify="right")
    t.add_column("Status")
    for r in cov["requirements"]:
        ok = r["linked_tests"] > 0
        t.add_row(
            r["id"],
            str(r["linked_tests"]),
            "[green]covered[/green]" if ok else "[red]UNcovered[/red]",
        )
    console.print(t)
    console.print(f"Uncovered: {cov['uncovered_count']}")


def _print_report(report: Dict[str, Any]) -> None:
    summ = report.get("summary", {})
    header = Table(show_header=False, box=None)
    header.add_row("contract", str(report.get("contract", "")))
    header.add_row("run_id", str(report.get("run_id", "")))
    header.add_row("passed", str(summ.get("passed", 0)))
    header.add_row("failed", str(summ.get("failed", 0)))
    header.add_row("skipped", str(summ.get("skipped", 0)))
    header.add_row("error", str(summ.get("error", 0)))
    console.print(Panel(header, title="CDD Test Report"))

    # Warnings
    warnings = report.get("warnings", [])
    if warnings:
        for w in warnings:
            console.print(f"[yellow]⚠ {w.get('code')}: {w.get('message')}[/yellow]")

    results = report.get("results", [])
    if not results:
        return

    t = Table(title="Results")
    t.add_column("Test")
    t.add_column("Status")
    t.add_column("Requirement")
    t.add_column("Message")
    for r in results:
        status = r.get("status", "")
        color = {
            "pass": "green",
            "fail": "red",
            "skipped": "yellow",
            "error": "magenta",
        }.get(status, "white")
        t.add_row(
            r.get("id", ""),
            f"[{color}]{status}[/{color}]",
            r.get("requirement", "") or "",
            (r.get("message", "") or "")[:120],
        )
    console.print(t)
