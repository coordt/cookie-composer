"""Layer management."""
from typing import Mapping

import logging
import os
import shutil
import tempfile
from enum import Enum
from pathlib import Path

from cookie_composer.composition import (
    LayerConfig,
    MergeStrategy,
    ProjectComposition,
    RenderedLayer,
    get_merge_strategy,
    write_composition,
)
from cookie_composer.data_merge import comprehensive_merge
from cookie_composer.matching import matches_any_glob
from cookie_composer.merge_files import MERGE_FUNCTIONS

from ._vendor.cookiecutter.config import get_user_config
from ._vendor.cookiecutter.generate import generate_context, generate_files
from ._vendor.cookiecutter.prompt import prompt_for_config
from ._vendor.cookiecutter.repository import determine_repo_dir
from ._vendor.cookiecutter.utils import rmtree

logger = logging.getLogger(__name__)


class WriteStrategy(Enum):
    """How to deal with a file."""

    WRITE = 1
    """Write or overwrite the file."""

    SKIP = 2
    """Skip the file."""

    MERGE = 3
    """Merge the file with an existing file, or write a new file."""


def render_layer(
    layer_config: LayerConfig, render_dir: Path, full_context: Mapping = None
) -> RenderedLayer:
    """
    Process one layer of the template composition.

    Renders the template using cookiecutter

    Args:
        layer_config: The configuration of the layer to render
        render_dir: Where to render the template
        full_context: The extra context from all layers in the composition

    Returns:
        The rendered layer information
    """
    config_dict = get_user_config(config_file=None, default_config=False)

    repo_dir, cleanup = determine_repo_dir(
        template=layer_config.template,
        abbreviations=config_dict["abbreviations"],
        clone_to_dir=config_dict["cookiecutters_dir"],
        checkout=layer_config.commit or layer_config.checkout,
        no_input=layer_config.no_input,
        password=layer_config.password,
        directory=layer_config.directory,
    )
    context = generate_context(
        context_file=Path(layer_config.template) / "cookiecutter.json",
        default_context=config_dict["default_context"],
        extra_context=full_context,
    )
    context["cookiecutter"] = prompt_for_config(context, layer_config.no_input)

    # TODO: Get the latest commit, if it is a git repository
    latest_commit = None

    rendered_layer = RenderedLayer(
        layer=layer_config,
        location=render_dir,
        new_context=context["cookiecutter"],
        latest_commit=latest_commit,
    )

    # call cookiecutter's generate files function
    generate_files(
        repo_dir=repo_dir,
        context=context,
        overwrite_if_exists=False,
        output_dir=str(render_dir),
    )

    if cleanup:
        rmtree(repo_dir)

    return rendered_layer


def merge_layers(destination: Path, rendered_layer: RenderedLayer):
    """
    Merge a layer into another layer using the rules specified in the layer_config.

    Args:
        destination: The root path to merge into.
        rendered_layer: The information about the rendered layer.
    """
    for root, dirs, files in os.walk(rendered_layer.location):
        rel_root = Path(root).relative_to(rendered_layer.location)

        for f in files:
            dest_path = destination / rel_root / f
            origin_path = Path(f"{root}/{f}")
            write_strat = get_write_strategy(origin_path, dest_path, rendered_layer)
            if write_strat == WriteStrategy.MERGE:
                merge_strategy = get_merge_strategy(
                    origin_path, rendered_layer.layer.merge_strategies
                )
                MERGE_FUNCTIONS[dest_path.suffix](
                    origin_path, dest_path, merge_strategy
                )
            elif write_strat == WriteStrategy.WRITE:
                shutil.copy(origin_path, dest_path)

        for d in dirs:
            dest_path = destination / rel_root / d
            origin_path = Path(f"{root}/{d}")
            write_strat = get_write_strategy(origin_path, dest_path, rendered_layer)
            if write_strat in {WriteStrategy.WRITE, WriteStrategy.MERGE}:
                dest_path.mkdir(parents=True, exist_ok=True)


def get_write_strategy(
    origin: Path, destination: Path, rendered_layer: RenderedLayer
) -> WriteStrategy:
    """
    Based on the layer_config rules, determine if we should overwrite an existin path.

    Args:
        origin: Path within the rendered layer that we are evaluating.
        destination: Path to which we would write this file (may not actually exist)
        rendered_layer: Rendered layer configuration.

    Returns:
        The appropriate way to handle writing this file.
    """
    if matches_any_glob(origin, rendered_layer.layer.skip_generation):
        logger.debug(f"{origin} matches a skip_generation pattern. Skipping.")
        return WriteStrategy.SKIP

    if not destination.exists():
        logger.debug(f"{destination} does not exist. Writing.")
        return WriteStrategy.WRITE

    merge_strat = get_merge_strategy(origin, rendered_layer.layer.merge_strategies)
    if merge_strat != MergeStrategy.DO_NOT_MERGE:
        logger.debug("Strategy is not do-not-merge. Merging.")
        return WriteStrategy.MERGE
    logger.debug("Strategy is do-not-merge. Continuing evaluation.")

    if matches_any_glob(origin, rendered_layer.layer.overwrite_exclude):
        logger.debug(f"{origin} matches an overwrite_exclude pattern. Skipping.")
        return WriteStrategy.SKIP

    if matches_any_glob(origin, rendered_layer.layer.overwrite):
        logger.debug(f"{origin} matches an overwrite pattern. Writing.")
        return WriteStrategy.WRITE

    if rendered_layer.layer.skip_if_file_exists:
        logger.debug("skip_if_file_exists is True. Skipping.")
        return WriteStrategy.SKIP
    else:
        logger.debug("skip_if_file_exists is False. Writing.")
        return WriteStrategy.WRITE


def process_composition(composition: ProjectComposition):
    """Process the composition."""
    full_context = {}
    rendered_layers = []

    for layer_config in composition.layers:
        if layer_config.context:
            full_context = comprehensive_merge(full_context, layer_config.context)

        with tempfile.TemporaryDirectory() as render_dir:
            rendered_layer = render_layer(layer_config, render_dir, full_context)
            merge_layers(composition.destination, rendered_layer)
        rendered_layers.append(rendered_layer)
        full_context = comprehensive_merge(full_context, rendered_layer.new_context)

    layers = []
    for rendered_layer in rendered_layers:
        rendered_layer.layer.commit = rendered_layer.latest_commit
        layers.append(rendered_layer.layer)

    composition_file = composition.destination / ".composition.yaml"
    write_composition(layers, composition_file)