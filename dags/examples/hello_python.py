# -*- coding: utf-8 -*-
"""
Airflow 3 Simple DAG: PythonOperator "Hello World"
--------------------------------------------------
Purpose
-------
Minimal, production-friendly example showing how to use a PythonOperator in Airflow 3.

Why this is "Airflow 3 ready"
-----------------------------
- No direct DB access or legacy patterns.
- Explicit DAG configuration (no implicit globals).
- Timezone-aware `start_date` (Pendulum) and `schedule=None` to avoid accidental backfills.
- `catchup=False` prevents historical runs unless explicitly triggered.
- Clear naming, tags, retry policy, and UI documentation (`doc_md`).
- Returns a value to XCom for observability/debug.

Usage
-----
1. Drop this file into your `dags/` directory (e.g. `dags/hello_python.py`).
2. Start the stack (e.g. `./run-airflow.sh` then open http://localhost:8080).
3. Trigger the DAG manually from the UI or via the CLI:
   `airflow dags trigger hello_python`
"""
from __future__ import annotations

import logging
from typing import Any, Dict

import pendulum
from airflow import DAG
from airflow.operators.python import PythonOperator, get_current_context

# ---------------------------------------------------------------------------
# DAG-level documentation (shown in the Airflow UI)
# ---------------------------------------------------------------------------
DAG_DOC = """
### Hello Python

A tiny DAG that runs a single `PythonOperator` printing **Hello World** and
returning a message to **XCom**. It also shows how to access the runtime
context (e.g., `run_id`, `logical_date`) via `get_current_context()`.

**Key points**
- Safe defaults (manual schedule, no catchup).
- Clear retry policy.
- Jinja templating on kwargs is supported via the Operator (not needed here).
"""

# ---------------------------------------------------------------------------
# Task callable
# ---------------------------------------------------------------------------
def hello(name: str = "World") -> str:
    """Simple callable for PythonOperator.

    Args:
        name: Who to greet.

    Returns:
        A greeting string (also pushed to XCom automatically).
    """
    log = logging.getLogger(__name__)

    # Access run-time context safely (Airflow 3-friendly)
    ctx: Dict[str, Any] = get_current_context()  # type: ignore[assignment]
    run_id = ctx.get("run_id")
    dag_id = ctx.get("dag").dag_id if ctx.get("dag") else "unknown_dag"
    ts = ctx.get("ts")  # ISO logical date

    message = f"👋 Hello {name}! (dag={dag_id}, run_id={run_id}, ts={ts})"
    log.info(message)
    print(message)  # visible in task logs

    # Returning a value stores it in XCom (good for debugging / chaining)
    return message


# ---------------------------------------------------------------------------
# DAG configuration
# ---------------------------------------------------------------------------
dag = DAG(
    dag_id="hello_python",
    description="Minimal PythonOperator DAG (Airflow 3 best practices)",
    start_date=pendulum.datetime(2025, 1, 1, tz="UTC"),  # timezone-aware
    schedule=None,              # run manually; avoids accidental backfills
    catchup=False,              # do not backfill past dates
    max_active_runs=1,          # one run at a time for simplicity
    default_args={
        "owner": "data-platform",
        "retries": 1,
        "retry_delay": pendulum.duration(minutes=2),
    },
    tags=["example", "python", "hello-world"],
    doc_md=DAG_DOC,
)

# ---------------------------------------------------------------------------
# Tasks
# ---------------------------------------------------------------------------
with dag:
    hello_task = PythonOperator(
        task_id="hello_world",
        python_callable=hello,
        op_kwargs={"name": "World"},  # change or template if needed
        doc_md="""
        #### Task: hello_world
        Calls a small Python function that:
        - Logs and prints a greeting
        - Shows runtime context (dag_id, run_id, ts)
        - Returns the greeting string to XCom
        """
    )

    # If you later add multiple tasks, declare dependencies like:
    # task_a >> task_b