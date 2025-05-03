import os
import copy
from sys import stdout
from typing import Any
DISABLE_ANSI = False


def disable_ansi():
    global DISABLE_ANSI
    DISABLE_ANSI = True

def bold(text: str) -> str:
    """Returns the text in bold format for terminal display."""
    if DISABLE_ANSI:
        return text
    else:
        return f'\033[1m{text}\033[0m'

def annotate_matrix(to_annotate: list[list[Any]], annotation_charset: list[Any] = None) -> list[list[Any]]:
    if not annotation_charset:
        annotation_charset = ["s"] + [chr(l + 96) for l in range(1, len(to_annotate) - 1)] + ["t"]

    annotated_version = copy.deepcopy(to_annotate)

    # Replace 0s with "*"
    for i in range(len(annotated_version)):
        for j in range(len(annotated_version[i])):
            if annotated_version[i][j] == 0:
                annotated_version[i][j] = " "  # Replace 0 with "*"

    # Add headers
    header_row = [" "] + annotation_charset
    header_col_cells = annotation_charset

    annotated_version.insert(0, header_row)

    for i, row in enumerate(annotated_version[1:]):
        row.insert(0, header_col_cells[i])

    return annotated_version


def print_matrix(matrix, cell_padding=2, header_row=True, header_column=True, output_file=stdout) -> None:
    N = len(matrix)
    M = len(matrix[0])
    border_top = '┏'  # Top border of the table
    row_sep = '┣'  # Separator between each row
    border_bot = '┗'  # Bottom border of the table
    col_lengths = []  # Represents the length of each column, based on the length of its longest cell
    # This generates the top, bottom, and separator lines to correctly align with the size of each cell.
    for i in range(M):
        max_cell_length = max([len(str(matrix[j][i])) for j in range(N)]) + cell_padding * 2
        col_lengths.append(max_cell_length)
        line = '━' * max_cell_length
        border_top += line + '┳'
        row_sep += line + '╋'
        border_bot += line + '┻'
    # We replace the last character with a closing character instead of the previous connecting ones
    border_top = border_top[:-1] + '┓'
    row_sep = row_sep[:-1] + '┫'
    border_bot = border_bot[:-1] + '┛'
    print(border_top, file=output_file)
    # This loop displays each row of the table
    for i in range(N):
        line = matrix[i]
        row = '┃'
        for j in range(M):
            cell = line[j]
            padded = str(line[j]).center(col_lengths[j], ' ')
            if i == 0 and header_row or j == 0 and header_column:
                padded = bold(padded)
            row += padded + '┃'
        print(row, file=output_file)
        if i + 1 < N:  # We print a separator after each row, except the last one since the bottom border comes afterwards
            print(row_sep, file=output_file)
    print(border_bot, file=output_file)
