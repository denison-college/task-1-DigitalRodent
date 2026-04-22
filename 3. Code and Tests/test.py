import builtins
import importlib
import json
import os
import runpy
import time
from datetime import datetime

import pytest


@pytest.fixture
def main_module(monkeypatch):
    monkeypatch.setattr(time, "sleep", lambda *_args, **_kwargs: None)
    monkeypatch.setattr(builtins, "input", lambda *_args, **_kwargs: "3")
    monkeypatch.setattr(os, "system", lambda *_args, **_kwargs: 0)
    return runpy.run_path("main.py")


@pytest.fixture
def game():
    return importlib.import_module("game")


@pytest.fixture
def score():
    return importlib.import_module("score")


@pytest.fixture
def temp_score_file(tmp_path, score, monkeypatch):
    score_file = tmp_path / "scores.json"
    monkeypatch.setattr(score, "SCORE_FILE", str(score_file))
    return score_file


def test_main_text_print_outputs_characters(main_module, monkeypatch, capsys):
    monkeypatch.setattr(time, "sleep", lambda *_args, **_kwargs: None)

    main_module["text_print"]("abc", 0)

    assert capsys.readouterr().out == "abc"


def test_main_clear_screen_calls_os_system(main_module, monkeypatch):
    called = {}

    def fake_system(command):
        called["command"] = command
        return 0

    monkeypatch.setattr(os, "system", fake_system)

    main_module["clear_screen"]()

    assert called["command"] in {"cls", "clear"}


def test_mainmenu_exit_option(monkeypatch, capsys):
    inputs = iter(["3"])
    monkeypatch.setattr(builtins, "input", lambda *_args, **_kwargs: next(inputs))
    monkeypatch.setattr(time, "sleep", lambda *_args, **_kwargs: None)
    monkeypatch.setattr(os, "system", lambda *_args, **_kwargs: 0)

    runpy.run_path("main.py")

    out = capsys.readouterr().out
    assert "Options" in out
    assert "Exit" in out


def test_game_choose_difficulty_retries_until_valid(game, monkeypatch):
    inputs = iter(["9", "2"])
    monkeypatch.setattr(builtins, "input", lambda *_args, **_kwargs: next(inputs))
    assert game.chooseDifficulty() == "Hurt Me Plenty"


def test_game_create_game_logic_places_mines_and_counts(game, monkeypatch):
    difficulty = {"Test": {"Rows": 2, "Cols": 2, "Mines": 1}}
    placements = iter([0, 0])

    monkeypatch.setattr(game.random, "randint", lambda *_args, **_kwargs: next(placements))

    logic = game.createGameLogic("Test", difficulty)
    assert logic == [["X", "1"], ["1", "1"]]


def test_game_create_game_dict_structure(game):
    grid = [["X", "1"], [" ", "2"]]
    result = game.createGameDict(grid)

    assert result[(0, 0)] == {"cell Ref": "A1", "Cell Value": "X", "Cell Vis": "Hidden"}
    assert result[(0, 1)]["cell Ref"] == "B1"
    assert result[(1, 0)]["cell Ref"] == "A2"


def test_game_make_selection_supports_flag_forms(game, monkeypatch):
    gamedict = {
        (0, 0): {"cell Ref": "A1", "Cell Value": " ", "Cell Vis": "Hidden"},
        (0, 1): {"cell Ref": "B1", "Cell Value": "X", "Cell Vis": "Hidden"},
    }

    inputs = iter(["F A1"])
    monkeypatch.setattr(builtins, "input", lambda *_args, **_kwargs: next(inputs))
    assert game.makeSelection(gamedict) == ((0, 0), "flag")

    inputs = iter(["flag B1"])
    monkeypatch.setattr(builtins, "input", lambda *_args, **_kwargs: next(inputs))
    assert game.makeSelection(gamedict) == ((0, 1), "flag")


def test_game_make_selection_rejects_invalid_then_accepts(game, monkeypatch, capsys):
    gamedict = {
        (0, 0): {"cell Ref": "A1", "Cell Value": " ", "Cell Vis": "Hidden"},
    }

    inputs = iter(["Z9", "A1"])
    monkeypatch.setattr(builtins, "input", lambda *_args, **_kwargs: next(inputs))

    assert game.makeSelection(gamedict) == ((0, 0), "uncover")
    assert "Invalid cell reference" in capsys.readouterr().out


def test_game_process_selection_flag_unflag_and_uncover(game, capsys):
    gameLogic = [[" ", "1"], ["1", "1"]]
    gameDict = {
        (0, 0): {"cell Ref": "A1", "Cell Value": " ", "Cell Vis": "Hidden"},
        (0, 1): {"cell Ref": "B1", "Cell Value": "1", "Cell Vis": "Hidden"},
        (1, 0): {"cell Ref": "A2", "Cell Value": "1", "Cell Vis": "Hidden"},
        (1, 1): {"cell Ref": "B2", "Cell Value": "1", "Cell Vis": "Hidden"},
    }

    game.processSelection((0, 0), "flag", gameLogic, gameDict)
    assert gameDict[(0, 0)]["Cell Vis"] == "Flagged"

    game.processSelection((0, 0), "flag", gameLogic, gameDict)
    assert gameDict[(0, 0)]["Cell Vis"] == "Hidden"

    game.processSelection((0, 0), "uncover", gameLogic, gameDict)
    assert gameDict[(0, 0)]["Cell Vis"] == "Uncovered"

    out = capsys.readouterr().out
    assert "flagged" in out
    assert "unflagged" in out


def test_game_process_selection_prevents_invalid_actions(game, capsys):
    gameLogic = [["1"]]
    gameDict = {(0, 0): {"cell Ref": "A1", "Cell Value": "1", "Cell Vis": "Uncovered"}}

    game.processSelection((0, 0), "flag", gameLogic, gameDict)
    assert "cannot flag" in capsys.readouterr().out.lower()

    gameDict[(0, 0)]["Cell Vis"] = "Flagged"
    game.processSelection((0, 0), "uncover", gameLogic, gameDict)
    assert "flagged" in capsys.readouterr().out.lower()

    gameDict[(0, 0)]["Cell Vis"] = "Uncovered"
    game.processSelection((0, 0), "uncover", gameLogic, gameDict)
    assert "already uncovered" in capsys.readouterr().out.lower()


def test_game_count_functions_and_elapsed_time(game):
    gameDict = {
        (0, 0): {"Cell Value": " ", "Cell Vis": "Hidden"},
        (0, 1): {"Cell Value": "X", "Cell Vis": "Hidden"},
        (1, 0): {"Cell Value": "1", "Cell Vis": "Flagged"},
        (1, 1): {"Cell Value": "2", "Cell Vis": "Uncovered"},
    }

    assert game.countRemainingCells(gameDict) == 1
    assert game.countFlags(gameDict) == 1
    assert game.formatElapsedTime(0) == "00:00.00"
    assert game.formatElapsedTime(65.4) == "01:05.40"
    assert game.formatElapsedTime(600.0) == "10:00.00"


def test_game_reveal_all_mines(game):
    gameDict = {
        (0, 0): {"Cell Value": "X", "Cell Vis": "Hidden"},
        (0, 1): {"Cell Value": "1", "Cell Vis": "Hidden"},
        (1, 0): {"Cell Value": "X", "Cell Vis": "Flagged"},
    }

    game.revealAllMines(gameDict)

    assert gameDict[(0, 0)]["Cell Vis"] == "Uncovered"
    assert gameDict[(1, 0)]["Cell Vis"] == "Uncovered"
    assert gameDict[(0, 1)]["Cell Vis"] == "Hidden"


def test_game_check_all_adjacent_cells_recursively_reveals_empty_area(game):
    gameLogic = [
        [" ", " ", "1"],
        [" ", "1", "1"],
        ["1", "1", "X"],
    ]
    gameDict = {
        (0, 0): {"Cell Vis": "Hidden"},
        (0, 1): {"Cell Vis": "Hidden"},
        (0, 2): {"Cell Vis": "Hidden"},
        (1, 0): {"Cell Vis": "Hidden"},
        (1, 1): {"Cell Vis": "Hidden"},
        (1, 2): {"Cell Vis": "Hidden"},
        (2, 0): {"Cell Vis": "Hidden"},
        (2, 1): {"Cell Vis": "Hidden"},
        (2, 2): {"Cell Vis": "Hidden"},
    }

    game.checkAllAdjacentCells((0, 0), gameLogic, gameDict)

    assert gameDict[(0, 1)]["Cell Vis"] == "Uncovered"
    assert gameDict[(1, 0)]["Cell Vis"] == "Uncovered"
    assert gameDict[(1, 1)]["Cell Vis"] == "Uncovered"
    assert gameDict[(2, 2)]["Cell Vis"] == "Hidden"


def test_game_print_game_screen_shows_board_state(game, monkeypatch, capsys):
    monkeypatch.setattr(game, "chooseDif", "Test")
    monkeypatch.setattr(game, "difficulty", {"Test": {"Mines": 1}})

    monkeypatch.setattr(time, "perf_counter", lambda: 10.0)

    gameLogic = [["1", "X"]]
    gameDict = {
        (0, 0): {"Cell Vis": "Uncovered"},
        (0, 1): {"Cell Vis": "Flagged"},
    }

    game.printGameScreen(gameLogic, gameDict, startTime=7.5)

    out = capsys.readouterr().out
    assert "Cells Remaining:" in out
    assert "Flags Placed:" in out
    assert "Flags Remaining:" in out
    assert "Time Elapsed:" in out
    assert "F" in out
    assert "1" in out


def test_game_check_for_win_lose_win(game, monkeypatch):
    monkeypatch.setattr(game, "chooseDif", "Test")
    monkeypatch.setattr(game, "difficulty", {"Test": {"Rows": 1, "Cols": 2, "Mines": 1}})

    saved = {}
    monkeypatch.setattr(game, "saveResult", lambda result, startTime: saved.update({"result": result}))
    monkeypatch.setattr(game, "printGameScreen", lambda *_args, **_kwargs: None)
    monkeypatch.setattr(time, "sleep", lambda *_args, **_kwargs: None)

    gameLogic = [["X", " "]]
    gameDict = {
        (0, 0): {"Cell Value": "X", "Cell Vis": "Hidden"},
        (0, 1): {"Cell Value": " ", "Cell Vis": "Uncovered"},
    }

    assert game.checkForWinLose(gameLogic, gameDict, 0.0) is False
    assert saved["result"] == "Won"


def test_game_check_for_win_lose_loss(game, monkeypatch):
    monkeypatch.setattr(game, "chooseDif", "Test")
    monkeypatch.setattr(game, "difficulty", {"Test": {"Rows": 1, "Cols": 2, "Mines": 1}})

    saved = {}
    monkeypatch.setattr(game, "saveResult", lambda result, startTime: saved.update({"result": result}))
    monkeypatch.setattr(game, "printGameScreen", lambda *_args, **_kwargs: None)
    monkeypatch.setattr(time, "sleep", lambda *_args, **_kwargs: None)

    gameLogic = [["X", " "]]
    gameDict = {
        (0, 0): {"Cell Value": "X", "Cell Vis": "Uncovered"},
        (0, 1): {"Cell Value": " ", "Cell Vis": "Hidden"},
    }

    assert game.checkForWinLose(gameLogic, gameDict, 0.0) is False
    assert saved["result"] == "Lost"


def test_score_load_scores_missing_file_returns_empty(score, temp_score_file):
    assert score.load_scores() == []


def test_score_load_scores_invalid_json_returns_empty(score, temp_score_file):
    temp_score_file.write_text("{not valid json}", encoding="utf-8")
    assert score.load_scores() == []


def test_score_load_scores_non_list_returns_empty(score, temp_score_file):
    temp_score_file.write_text(json.dumps({"name": "Alice"}), encoding="utf-8")
    assert score.load_scores() == []


def test_score_save_scores_writes_pretty_json(score, temp_score_file):
    payload = [{"name": "A", "result": "Won"}]
    score.save_scores(payload)

    text = temp_score_file.read_text(encoding="utf-8")
    assert json.loads(text) == payload
    assert "\n    {" in text


def test_score_score_key_prioritizes_wins_then_time(score):
    assert score._score_key({"result": "Won", "time": 5}) < score._score_key({"result": "Lost", "time": 1})
    assert score._score_key({"result": "Won", "time": 5}) < score._score_key({"result": "Won", "time": 9})


def test_score_add_score_normalizes_fields_and_limits_to_max(score, monkeypatch):
    saved = {}

    existing = [
        {"name": f"Player{i}", "result": "Lost", "difficulty": "D", "time": i, "date": "2024-01-01 00:00:00"}
        for i in range(20)
    ]
    monkeypatch.setattr(score, "load_scores", lambda: list(existing))
    monkeypatch.setattr(score, "save_scores", lambda data: saved.update({"data": data}))
    monkeypatch.setattr(score, "datetime", datetime)

    score.add_score("  Bob  ", "won", 12.3456, " Hard ")

    assert len(saved["data"]) == score.MAX_HIGHSCORES
    assert saved["data"][0]["name"] == "Bob"
    assert saved["data"][0]["result"] == "Won"
    assert saved["data"][0]["difficulty"] == "Hard"
    assert saved["data"][0]["time"] == 12.35
    assert "date" in saved["data"][0]


def test_score_add_score_uses_unknown_for_blank_name(score, monkeypatch):
    saved = {}
    monkeypatch.setattr(score, "load_scores", lambda: [])
    monkeypatch.setattr(score, "save_scores", lambda data: saved.update({"data": data}))
    monkeypatch.setattr(score, "datetime", datetime)

    score.add_score("", "lost", 1, "Easy")

    assert saved["data"][0]["name"] == "Unknown"
    assert saved["data"][0]["result"] == "Lost"


def test_score_show_scoreboard_empty(score, monkeypatch, capsys):
    monkeypatch.setattr(score, "load_scores", lambda: [])
    score.show_scoreboard()

    out = capsys.readouterr().out
    assert "FINAL HIGHSCORES" in out
    assert "No highscores have been recorded yet." in out


def test_score_show_scoreboard_formats_and_sorts(score, monkeypatch, capsys):
    monkeypatch.setattr(
        score,
        "load_scores",
        lambda: [
            {"name": "VeryLongPlayerNameHere", "result": "Lost", "difficulty": "Ultra-Violence", "time": 2.0, "date": "2024-01-02 00:00:00"},
            {"name": "Bob", "result": "Won", "difficulty": "Easy", "time": 9.0, "date": "2024-01-01 00:00:00"},
            {"name": "Alice", "result": "Won", "difficulty": "Easy", "time": 3.0, "date": "2024-01-03 00:00:00"},
        ],
    )

    score.show_scoreboard()

    out = capsys.readouterr().out
    assert "Bob" in out
    assert "Alice" in out
    assert "VeryLongPlayerNam" in out
    assert out.index("Bob") < out.index("Alice") < out.index("VeryLongPlayerNam")


def test_score_clear_scores(score, monkeypatch):
    saved = {}
    monkeypatch.setattr(score, "save_scores", lambda data: saved.update({"data": data}))

    score.clear_scores()

    assert saved["data"] == []