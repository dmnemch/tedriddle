# The TED riddle for inspiration: https://www.youtube.com/watch?v=qgvmJTmJIKs

import random
import plotly.express as px
import argparse
import pandas as pd
import os
import subprocess
import numpy as np


def get_args():
    parser = argparse.ArgumentParser(
        prog="strange_numbers",
    )
    parser.add_argument('-m', '--max', help="maximum number to iterate to")
    return parser.parse_args()


def get_rand_color(): # actually I don't use this function :)
    col = "#"
    for i in range(6):
        col += random.choice("0123456789ABCDEF")
    return col


def generate_df(max):
    """
    Generates scratch of df (like in the TED video), then modifided by het 
    """
    i = 3
    _ = pd.DataFrame([[1, 2, 3], [2, 3, 6]])
    while i * 3 < max:
        if not _.loc[_[1] == i][2].empty:
            next_row = pd.DataFrame([i, int(_.loc[_[1] == i][2]), i * 3]).T
            _ = pd.concat([_, next_row], ignore_index=True)

            # this peace of func fills in the gaps in previous rows
            if _[1][i-2] == 0:
                index = i - 2
                while _[1][index] == 0:
                    index -= 1
                if (_[1][i-1] - _[1][index]) == (i-1-index):
                    index += 1
                    while index != (i-1):
                        _[1][index] = _[1][index-1] + 1
                        index += 1

        else:
            next_row = pd.DataFrame(data=[i, 0, i * 3]).T
            _ = pd.concat([_, next_row], ignore_index=True)
        i += 1
    return _


def get_lines(df):
    """
    Gets lines to color them in one
    """
    lines = [[]]
    for x in df.T:
        if x + 1 not in np.concatenate(lines, axis=0):
            line = []
            next = x
            while next < len(df):
                for y in df.T[next]:
                    line.append(y)
                next = line[-1] -1
            lines.append((sorted(list(set(line)))))
        else:
            continue
    return lines[1::]


def get_func_df(df, max):
    """
    Creates df with x, y and color group based on get_lines func
    """
    func_df = pd.DataFrame()
    for x in df.T:
        next_row = pd.DataFrame([df.T[x][0], df.T[x][1]]).T
        func_df = pd.concat([next_row, func_df], ignore_index=True)
        next_row = pd.DataFrame([df.T[x][1], df.T[x][2]]).T
        func_df = pd.concat([next_row, func_df], ignore_index=True)
    func_df.rename(columns={0: 'x', 1: 'y'}, inplace=True)

    lines = get_lines(df)
    func_df['line'] = -1
    for i, line in enumerate(lines):
        for x in line:
            func_df['line'][func_df[func_df['x'] == x].index] = i

    func_df['line'] = func_df['line'].astype(str)
    func_df = func_df[func_df['x'] < max//3]
    return func_df


def save_plotly(fig, file="out.html"):
    """
    Saves *fig* to *file* (destination) and opens it in default html app
    """
    fig.write_html(file)
    try:
        os.startfile(file)
    except AttributeError:
        try:
            subprocess.call(['open', file])
        except:
            raise Exception('Could not open file')

            
def main():
    args = get_args()
    max = int(args.max) * 3
    df = generate_df(max)
    func_df = get_func_df(df, max)
    fig = px.scatter(func_df, x='x', y='y', color='line')
    fig.update(layout_showlegend=False)
    save_plotly(fig)

if __name__ == '__main__':
    main()
