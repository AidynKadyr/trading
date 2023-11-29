# -*- coding: utf-8 -*-
import pandas as pd
import re
from pathlib import Path
import os


def get_macro_data(start_date, end_date, *countries):
    start_date = start_date.replace("/", "-")
    end_date = end_date.replace("/", "-")
    # should change absolute path if you move file
    cdir = Path().resolve()
    macroData = pd.DataFrame()
    for country in countries:
        dataPath = f"{cdir}/datasets/macroeconomic/{country}/"
        for path in Path(dataPath).rglob("*.csv"):
            df = pd.DataFrame()
            columName = country.lower() + "_" + re.sub(r"\..*", "", path.name)
            df[columName] = pd.read_csv(f"{path}", index_col=0)
            df.index = pd.to_datetime(df.index)

            df = df.resample("D").interpolate()
            df["week"] = pd.to_datetime(df.index).day_name()
            df = df.query("week not in ['Saturday', 'Sunday']")
            df = df.drop(["week"], axis=1)
            df = df[start_date:end_date]
            macroData[columName] = df
            macroData.index.name = "date"
    return macroData
