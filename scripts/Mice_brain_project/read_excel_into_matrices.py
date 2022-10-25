#########################################################################
# DESCRIPTION: alternative script for parsing document: brain_data.xlsx #
#########################################################################
#Usage: python read_excel_into_matrices.py making sure that the following path is correct

# 1. The script initializes one dictionary, called "brain", with three entries: "left",
# "right" and "mean". These will each contain a (single) dataframe whose rows are the
# different times (0.0, 0.5, 1.0, 2.0, 6.0, 24.0) and whose columns are the 639 regions.

# Each entry in the dataframe is the average percentage at the corresponding time in
# the corresponding region (for "left" and "right") and the average of the left and
# right sides (for "mean").

import pandas as pd
import numpy as np

# Create a dictionary ("raw_brain") of dataframes, whose keys are the names of the Excel
# sheets
raw_brain = pd.read_excel("/home/rafael/Postdoc/IKUR/brain_data.xlsx", sheet_name = None)

# Change the keys' names, to make sure they are the same as the regions' names
# (the "Recovered Sheet" keys are not)
new_keys = [list(set([region for region in raw_brain[key].values[:, 1] \
            if not pd.isna(region)]))[0] for key in list(raw_brain.keys())]

raw_brain = dict(zip(new_keys, list(raw_brain.values())))

times = [0.0, 0.5, 1.0, 2.0, 6.0, 24.0]
regions = list(raw_brain.keys())
sides = ["left", "right"]

# Replace the times' columns in the Excel file (which are strings) with actual floating numbers
for region in regions:
    raw_brain[region] = raw_brain[region].replace(["pseudo", "0.5h", "1h", "2h", "6h", "24h"], times)

# Create a dictionary ("brain") with three keys ("left", "right" and "mean")
# The values of "left" and "right" are a single dataframe (a matrix of (times, regions))
# The value of "mean" is a dataframe containing the average matrix.
brain = dict()
brain["left"] = pd.DataFrame(index = times, columns = regions)
brain["right"] = pd.DataFrame(index = times, columns = regions)
brain["mean"] = pd.DataFrame(index = times, columns = regions)

for region in regions:
    for time in times:
        for side in sides:
            brain[side][region][time] = np.mean(raw_brain[region].loc[(raw_brain[region]["time"] == time) & \
            (raw_brain[region]["side"] == side) & (raw_brain[region]["percent"] <= 100.0) & \
            ~(pd.isna(raw_brain[region]["exp"])), ["percent"]], axis = 0).values[0]
        if not pd.isna(brain["left"][region][time]) and not pd.isna(brain["right"][region][time]):
            brain["mean"][region][time] = 0.5 * (brain["left"][region][time] + brain["right"][region][time])
        elif pd.isna(brain["left"][region][time]):
            brain["mean"][region][time] = brain["right"][region][time]
        else:
            brain["mean"][region][time] = brain["left"][region][time]

# Create a column with the times in each dataframe, by replacing the current "index" column
for side in ["left", "right", "mean"]:
    brain[side].reset_index(inplace = True)
    brain[side] = brain[side].rename(columns = {"index": "times"})

print(brain["mean"])
