from pathlib import Path
from dyslexia.eval.eval_utils import eval_txt_file, eval_folder

test_path = Path(__file__).resolve().parents[1]


def test_eval_txt_file():
    truth_path = test_path / "data" / "truth" / "example1.txt"
    hypothesis_path = test_path / "data" / "hypothesis" / "example1.txt"

    eval_dict = eval_txt_file(truth_path, hypothesis_path)

    assert "wer" in eval_dict


def test_eval_folder():
    truth_path = test_path / "data" / "truth"
    hypothesis_path = test_path / "data" / "hypothesis"

    eval_dict = eval_folder(truth_path, hypothesis_path)

    assert "wer" in eval_dict
