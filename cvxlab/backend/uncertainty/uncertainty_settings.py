"""Validated containers for uncertainty-analysis settings."""

from __future__ import annotations

from typing import Any

from cvxlab.defaults import Defaults
from cvxlab.log_exc.logger import Logger


class UncertaintySettings:
    """Validated container for uncertainty-analysis configuration.

    The class validates and stores the configuration used for uncertainty
    sampling, model-output collection, and global sensitivity analysis.

    Attributes:
        sampling_method: Selected SALib sampling method.
        gsa_method: Selected global sensitivity analysis method.
        sampling_kwargs: Keyword arguments passed to the SALib sampler.
        gsa_kwargs: Keyword arguments passed to the SALib analyzer.
        groups: Whether grouped sampling is enabled.
        measures: Uncertainty measures selected for GSA.
        scenarios: Scenarios selected for GSA.
        save_samples: Whether generated samples are exported.
        save_measures: Whether uncertainty measures are exported.
        save_analysis: Whether GSA results are exported.
        temp_save: Whether uncertainty measures are progressively saved.
        file_format: Output format used for exported dataframes.
    """

    def __init__(
        self,
        *,
        logger: Logger,
        uncertainty_enabled: bool,
        sampling_method: str,
        gsa_method: str,
        sampling_kwargs: dict[str, Any] | None = None,
        gsa_kwargs: dict[str, Any] | None = None,
        groups: bool = False,
        measures: list[str] | None = None,
        scenarios: list[str] | None = None,
        save_samples: bool = True,
        save_measures: bool = True,
        save_gsa: bool = True,
        temp_save: bool = True,
        file_format: Defaults.LiteralTypes.DataFileType | None = "xlsx",
    ) -> None:
        """Validate, normalize and store uncertainty-analysis settings."""

        # ------------------------------------------------------------------
        # Uncertainty-analysis availability
        # ------------------------------------------------------------------

        self.logger = logger

        if not uncertainty_enabled:
            raise ValueError(
                "Uncertainty analysis is not enabled. "
                "Create the model with "
                f"{Defaults.Labels.UNCERTAINTY_SETTING_KEY}=True."
            )

        # ------------------------------------------------------------------
        # Methods
        # ------------------------------------------------------------------

        if not isinstance(sampling_method, str):
            raise TypeError(
                "'sampling_method' must be a string."
            )

        if not isinstance(gsa_method, str):
            raise TypeError(
                "'gsa_method' must be a string."
            )

        sampling_method = sampling_method.lower()
        gsa_method = gsa_method.lower()

        # ------------------------------------------------------------------
        # Method kwargs
        # ------------------------------------------------------------------

        if sampling_kwargs is None:
            sampling_kwargs = {}
        elif not isinstance(sampling_kwargs, dict):
            raise TypeError(
                "'sampling_kwargs' must be a dictionary or None."
            )
        else:
            sampling_kwargs = sampling_kwargs.copy()

        if gsa_kwargs is None:
            gsa_kwargs = {}
            self.logger.warning(
                "Uncertainty analysis | No GSA method configured. "
                "Sampling and model runs will be completed without computing  global sensitivity analysis idexes."
            )
        elif not isinstance(gsa_kwargs, dict):
            raise TypeError(
                "'gsa_kwargs' must be a dictionary or None."
            )
        else:
            gsa_kwargs = gsa_kwargs.copy()

        # ------------------------------------------------------------------
        # Sampling configuration
        # ------------------------------------------------------------------

        if not isinstance(groups, bool):
            raise TypeError(
                "'groups' must be a boolean."
            )

        # ------------------------------------------------------------------
        # GSA targets
        # ------------------------------------------------------------------

        if measures is not None and not isinstance(measures, list):
            raise TypeError(
                "'measures' must be a list of strings or None."
            )

        if scenarios is not None and not isinstance(scenarios, list):
            raise TypeError(
                "'scenarios' must be a list of strings or None."
            )

        # ------------------------------------------------------------------
        # Saving configuration
        # ------------------------------------------------------------------

        if not isinstance(save_samples, bool):
            raise TypeError(
                "'save_samples' must be a boolean."
            )

        if not isinstance(save_measures, bool):
            raise TypeError(
                "'save_measures' must be a boolean."
            )

        if not isinstance(save_gsa, bool):
            raise TypeError(
                "'save_analysis' must be a boolean."
            )

        if not isinstance(temp_save, bool):
            raise TypeError(
                "'temp_save' must be a boolean."
            )

        if temp_save and not save_measures:
            raise ValueError(
                "Uncertainty settings | "
                "'temp_save=True' requires 'save_measures=True'."
            )

        # ------------------------------------------------------------------
        # File format
        # ------------------------------------------------------------------

        if file_format is not None:
            if not isinstance(file_format, str):
                raise TypeError(
                    "'file_format' must be a string or None."
                )

            file_format = file_format.lower()

            allowed_formats = (
                Defaults.UncertaintySettings.AVAILABLE_EXPORT_FORMATS
            )

            if file_format not in allowed_formats:
                raise ValueError(
                    f"Output format '{file_format}' is not supported. "
                    f"Available formats: {sorted(allowed_formats)}."
                )

        if not save_samples and file_format is not None:
            logger.warning(
                "Uncertainty settings | 'file_format' was specified while "
                "'save_samples=False'. Samples will not be saved."
            )

        if not save_measures and file_format is not None:
            logger.warning(
                "Uncertainty settings | 'file_format' was specified while "
                "'save_measures=False'. Measures will not be saved."
            )

        if not save_gsa and file_format is not None:
            logger.warning(
                "Uncertainty settings | 'file_format' was specified while "
                "'save_analysis=False'. GSA results will not be saved."
            )

        if not save_samples:
            logger.warning(
                "Uncertainty settings | Samples will not be saved."
            )

        if not save_measures:
            logger.warning(
                "Uncertainty settings | Measures will not be saved."
            )

        # ------------------------------------------------------------------
        # Store normalized settings
        # ------------------------------------------------------------------

        self.sampling_method = sampling_method
        self.gsa_method = gsa_method

        self.sampling_kwargs = sampling_kwargs
        self.gsa_kwargs = gsa_kwargs

        self.groups = groups
        self.measures = measures
        self.scenarios = scenarios

        self.save_samples = save_samples
        self.save_measures = save_measures
        self.save_gsa = save_gsa
        self.temp_save = temp_save

        self.file_format = file_format

    def __repr__(self) -> str:
        return (
            f"{type(self).__name__}("
            f"sampling_method='{self.sampling_method}', "
            f"gsa_method='{self.gsa_method}', "
            f"groups={self.groups}, "
            f"measures={self.measures}, "
            f"scenarios={self.scenarios}, "
            f"save_samples={self.save_samples}, "
            f"save_measures={self.save_measures}, "
            f"save_analysis={self.save_gsa}, "
            f"temp_save={self.temp_save}, "
            f"file_format={self.file_format!r})"
        )
