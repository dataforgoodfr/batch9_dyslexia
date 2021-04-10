import jiwer
from pathlib import Path
from typing import Mapping, Dict
import numpy as np


def eval_txt_file(ground_truth_path: Path, prediction_path: Path) -> Dict[str, float]:
    """

    :param ground_truth_path:
    :param prediction_path:
    :return:
    """
    with open(ground_truth_path, "r") as f:
        truth = f.read()

    with open(prediction_path, "r") as f:
        hypothesis = f.read()

    return dict(jiwer.compute_measures(truth=truth, hypothesis=hypothesis))


def eval_folder(ground_truth_path: Path, prediction_path: Path) -> Dict[str, float]:
    """

    :param ground_truth_path:
    :param prediction_path:
    :return:
    """

    truth_txt_paths = list(ground_truth_path.glob("*.txt"))
    hypothesis_txt_paths = [prediction_path / p.name for p in truth_txt_paths]

    results = [
        eval_txt_file(truth, hypothesis)
        for truth, hypothesis in zip(truth_txt_paths, hypothesis_txt_paths)
    ]

    aggragate_scores = {}

    for res, t, h in zip(results, truth_txt_paths, hypothesis_txt_paths):
        print(t, h, res)

    if results:
        for key in results[0]:
            aggragate_scores[key] = float(np.mean([d[key] for d in results]))

    return aggragate_scores
