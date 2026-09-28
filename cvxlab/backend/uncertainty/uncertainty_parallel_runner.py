from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path
import shutil

# import pandas as pd


class UncertaintyParallelRunner:
    """Manage parallel execution of uncertainty-analysis model runs.

    The class handles the internal orchestration required to execute uncertainty
    runs in separate processes. Each worker uses an isolated copy of the model
    SQLite database while sharing the same model structure and input files.

    The runner is responsible for:
    - creating worker directories and database copies;
    - distributing uncertainty run IDs among workers;
    - starting worker processes;
    - collecting completed run results;
    - registering results in the main model instance;
    - cleaning temporary worker files.

    The class is intended for internal use by ``Model.run_uncertainty()``.
    """

    def __init__(
        self,
        model,
        n_parallel: int,
    ) -> None:
        """Initialize the parallel uncertainty runner.

        Args:
            model: Main Model instance controlling the uncertainty analysis.
            n_parallel: Maximum number of uncertainty workers executed in parallel.

        Raises:
            ValueError: If ``n_parallel`` is smaller than one.
        """
        if n_parallel < 1:
            raise ValueError(
                "'n_parallel' must be greater than or equal to 1."
            )

        self.model = model
        self.n_parallel = n_parallel

        self.workers_dir = (
            self.model.paths.model_dir
            / "parallel_workers"
        )

        self.worker_dirs: list[Path] = []

    def _create_worker_dirs(
        self,
    ) -> list[Path]:
        """Create isolated directories and database copies for parallel workers.

        Returns:
            List of paths corresponding to the generated worker directories.
        """
        self.workers_dir.mkdir(exist_ok=True)

        self.worker_dirs = []

        for worker_id in range(self.n_parallel):

            worker_dir = (
                self.workers_dir
                / f"worker_{worker_id}"
            )

            worker_dir.mkdir(exist_ok=True)

            worker_database = (
                worker_dir
                / self.model.paths.sqlite_database.name
            )

            if worker_database.exists():
                worker_database.unlink()

            shutil.copy2(
                self.model.paths.sqlite_database,
                worker_database,
            )

            self.worker_dirs.append(worker_dir)

        return self.worker_dirs

    def _split_run_ids(
        self,
        run_ids,
    ) -> list[list[int]]:
        """Distribute uncertainty run IDs among available workers.

        Run IDs are distributed using a round-robin strategy so that consecutive
        runs are spread across different workers.

        Args:
            run_ids: Iterable containing the uncertainty run IDs to execute.

        Returns:
            List containing one list of run IDs for each worker.
        """

        run_ids = list(run_ids)

        return [
            run_ids[i::self.n_parallel]
            for i in range(self.n_parallel)
        ]

    def cleanup_worker_dirs(
        self,
    ) -> None:
        """Remove temporary directories created for parallel workers.

        The complete ``parallel_workers`` directory is deleted after the parallel
        uncertainty execution has completed or when execution is interrupted.
        """

        if self.workers_dir.exists():
            shutil.rmtree(self.workers_dir)

        self.worker_dirs = []

    def _get_worker_database_path(
        self,
        worker_id: int,
    ) -> Path:
        """Return the SQLite database path assigned to a worker.
        Args:
            worker_id: Identifier of the worker
        Returns:
            Path to the worker-specific SQLite database..
        """
        worker_dir = self.worker_dirs[worker_id]

        return (
            worker_dir
            / self.model.paths.sqlite_database.name
        )

    def _get_worker_samples(
        self,
        worker_run_ids: list[int],
    ):
        """Return uncertainty samples assigned to a worker.

        Args:
            worker_run_ids: Run IDs assigned to the worker.

        Returns:
            Copy of the uncertainty samples associated with the selected run IDs.
        """
        samples = self.model.core.uncertainty.uncertainty_samples

        run_id_col = (
            self.model.core.uncertainty
            .uncertainty_defaults.RUN_ID
        )

        worker_samples = samples.loc[
            samples[run_id_col].isin(worker_run_ids)
        ].copy()

        return worker_samples

    def _build_single_worker_config(
        self,
        worker_id: int,
        worker_run_ids: list[int],
    ) -> dict:
        """Build the configuration required by one uncertainty worker.

        Args:
            worker_id: Identifier of the worker.
            worker_run_ids: Run IDs assigned to the worker.

        Returns:
            Dictionary containing worker-specific execution data.
        """
        return {
            "run_ids": worker_run_ids,
            "samples": self._get_worker_samples(worker_run_ids),
            "database_path": self._get_worker_database_path(worker_id),
        }

    def _build_workers_configs(
        self,
        run_ids,
    ) -> list[dict]:
        """Build worker-specific configurations for parallel execution.

        Args:
            run_ids: Uncertainty run IDs to distribute among workers.

        Returns:
            List containing one configuration dictionary for each active worker.
        """
        split_run_ids = self._split_run_ids(run_ids)

        return [
            self._build_single_worker_config(
                worker_id=worker_id,
                worker_run_ids=worker_run_ids,
            )
            for worker_id, worker_run_ids in enumerate(split_run_ids)
            if worker_run_ids
        ]

    def _get_model_init_kwargs(self) -> dict:
        """Return common arguments required to initialize worker models.

        Returns:
            Dictionary containing the Model initialization arguments shared
            by all parallel workers.
        """
        return {
            "model_dir_name": self.model.settings.model_name,
            "main_dir_path": str(self.model.paths.model_dir.parent),
            "uncertainty": True,
            "use_existing_data": True,
            "log_level": self.model.settings.log_level,
        }

    def run_parallel(
        self,
        run_ids,
        run_kwargs: dict,
    ) -> list[tuple]:
        """Execute uncertainty runs using multiple worker processes."""

        self._create_worker_dirs()

        worker_configs = self._build_workers_configs(
            run_ids=run_ids,
        )

        model_init_kwargs = self._get_model_init_kwargs()

        results = []

        with ProcessPoolExecutor(
            max_workers=len(worker_configs)
        ) as executor:

            futures = [
                executor.submit(
                    _run_uncertainty_worker,
                    config,
                    model_init_kwargs,
                    run_kwargs,
                )
                for config in worker_configs
            ]

            for future in as_completed(futures):
                results.extend(future.result())

        results.sort(key=lambda result: result[0])

        return results


def _run_uncertainty_worker(
    config: dict,
    model_init_kwargs: dict,
    run_kwargs: dict,
) -> list[tuple]:
    """Execute uncertainty runs assigned to one worker process.

    Args:
        config: Worker-specific configuration containing run IDs,
            uncertainty samples, and database path.
        model_init_kwargs: Common arguments required to initialize
            the worker Model.
        run_kwargs: Arguments required to execute each uncertainty run.

    Returns:
        List of tuples containing run ID, measure records, and failed scenarios.
    """
    from cvxlab.backend.model import Model

    worker_model = Model(
        **model_init_kwargs,
        _sqlite_database_path=config["database_path"],
    )

    worker_model.core.uncertainty.uncertainty_samples = (
        config["samples"]
    )

    worker_model.core.initialize_problem_structure_and_load_deterministic_data(
        force_overwrite=True,
    )

    results = []

    for run_id in config["run_ids"]:

        run_records, failed_scenarios = (
            worker_model._run_uncertainty_sample(
                run_id=run_id,
                **run_kwargs,
            )
        )

        results.append(
            (
                run_id,
                run_records,
                failed_scenarios,
            )
        )

    return results
