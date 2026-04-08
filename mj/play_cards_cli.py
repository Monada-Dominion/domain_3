#!/usr/bin/env python3
"""Terminal card drawer for Mystical Journey cards.

Controls:
- g / Space / Enter: draw a random card
- r: reset deck and reshuffle
- q: quit
"""

from __future__ import annotations

import curses
import random
import re
import textwrap
from dataclasses import dataclass
from pathlib import Path
from typing import List


CARD_BLOCK_PATTERN = re.compile(
    r"^##\s+Card\s+(\d+)\s*$\n(.*?)(?=^##\s+Card\s+\d+\s*$|\Z)",
    re.MULTILINE | re.DOTALL,
)


@dataclass(frozen=True)
class Card:
    number: int
    text: str


def load_cards(cards_path: Path) -> List[Card]:
    content = cards_path.read_text(encoding="utf-8")
    cards = [
        Card(number=int(number), text=text.strip())
        for number, text in CARD_BLOCK_PATTERN.findall(content)
    ]
    if not cards:
        raise ValueError(
            f"No cards found in {cards_path}. Expected markdown sections like '## Card 1'."
        )
    return cards


def draw_header(stdscr: curses.window, width: int) -> None:
    title = "Mystical Journey - Card Drawer"
    controls = "[G/Enter/Space] Go   [R] Reset deck   [Q] Quit"
    stdscr.addstr(0, max(0, (width - len(title)) // 2), title, curses.A_BOLD)
    stdscr.addstr(1, max(0, (width - len(controls)) // 2), controls)
    stdscr.hline(2, 0, curses.ACS_HLINE, width)


def draw_centered_block(
    stdscr: curses.window,
    lines: List[str],
    top: int,
    bottom: int,
    width: int,
    attr: int = 0,
) -> None:
    if top >= bottom:
        return

    block_height = len(lines)
    start_y = top + max(0, (bottom - top - block_height) // 2)
    for i, line in enumerate(lines):
        y = start_y + i
        if y >= bottom:
            break
        x = max(0, (width - len(line)) // 2)
        stdscr.addnstr(y, x, line, max(0, width - 1), attr)


def draw_card_screen(
    stdscr: curses.window,
    current_card: Card | None,
    remaining: int,
    total: int,
) -> None:
    stdscr.erase()
    height, width = stdscr.getmaxyx()

    if height < 12 or width < 48:
        message = "Terminal too small. Resize to at least 48x12."
        draw_centered_block(stdscr, [message], 0, height, width, curses.A_BOLD)
        stdscr.refresh()
        return

    draw_header(stdscr, width)

    footer = f"Cards left in deck: {remaining}/{total}"
    stdscr.hline(height - 2, 0, curses.ACS_HLINE, width)
    stdscr.addstr(height - 1, max(0, (width - len(footer)) // 2), footer)

    card_top = 4
    card_bottom = height - 3

    if current_card is None:
        lines = [
            "Press GO to draw your first card",
            "The deck will not repeat cards until reset.",
        ]
        draw_centered_block(stdscr, lines, card_top, card_bottom, width)
    else:
        number_line = f"Card {current_card.number}"
        wrapped = textwrap.wrap(current_card.text, width=max(24, width - 8))
        lines = [number_line, ""] + wrapped
        draw_centered_block(stdscr, lines, card_top, card_bottom, width)

    stdscr.refresh()


def run_game(stdscr: curses.window, cards: List[Card]) -> None:
    curses.curs_set(0)
    stdscr.nodelay(False)
    stdscr.keypad(True)

    all_cards = cards[:]
    deck = cards[:]
    current_card: Card | None = None

    draw_card_screen(stdscr, current_card, len(deck), len(all_cards))

    while True:
        key = stdscr.getch()

        if key in (ord("q"), ord("Q")):
            return

        if key in (ord("r"), ord("R")):
            deck = all_cards[:]
            current_card = None
            draw_card_screen(stdscr, current_card, len(deck), len(all_cards))
            continue

        if key in (ord("g"), ord("G"), ord(" "), curses.KEY_ENTER, 10, 13):
            if not deck:
                deck = all_cards[:]
            current_card = deck.pop(random.randrange(len(deck)))
            draw_card_screen(stdscr, current_card, len(deck), len(all_cards))
            continue

        if key == curses.KEY_RESIZE:
            draw_card_screen(stdscr, current_card, len(deck), len(all_cards))


def main() -> None:
    cards_path = Path(__file__).with_name("cards.md")
    try:
        cards = load_cards(cards_path)
    except Exception as exc:
        raise SystemExit(f"Could not load cards: {exc}") from exc

    curses.wrapper(run_game, cards)


if __name__ == "__main__":
    main()
