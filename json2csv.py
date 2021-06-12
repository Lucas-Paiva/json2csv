# JSON converter to CSV

# Issues:
# 1 - Choose the name of the file - OK
# 2 - Choose the destiny of the file
# 3 - Choose the Encoding of the CSV
# 4 - Choose the Delimiter - OK
# 5 - Fix flattered & nested list issues
# 6 - Freeze all with cxfreeze
# 7 - Add 'Preview' tool
# 8 - Align all with columns

import json as jsn
import pandas as pd
import PySimpleGUI as sg
import os

menu_def = [
    [
        "Settings",
        ["Theme", "Encoding", "Default Destination"],
    ],
    ["Help", "&About..."],
]

sg.theme("SystemDefault1")

src = os.path.dirname(__file__) + "\\logo_json2csv_EXTENDED.png"
icon_src = os.path.dirname(__file__) + "\\icon.ico"

layout = [
    [sg.Menu(menu_def)],
    [sg.Image(src)],
    [
        sg.Text("JSON type:"),
        sg.Combo(["Flattened", "Nested"], enable_events=True, key="combo"),
        sg.Text("Delimiter: "),
        sg.Input(default_text=",", size=(3, 1), key="-DEL-"),
        sg.Text("Encoding: "),
        sg.Input(default_text="UTF8", size=(5, 1), key="-ENC-"),
    ],
    [
        sg.Text("Choosen file source: "),
        sg.Input(),
        sg.FileBrowse(key="-IN-"),
    ],
    [sg.Text("Converted File name: "), sg.Input(key="-NAME-"), sg.Text(".csv")],
    [sg.Text("Data preview"), sg.Output(size=(45, 5), key="_OUTPUT_")],
    [sg.Button("Preview"), sg.Button("Export"), sg.Button("Cancel")],
]

#  Building Window
window = sg.Window(
    "JSON2CSV Converter", layout, icon=icon_src, size=(600, 300), resizable=True
)


def countColumns(file):
    json = pd.read_json(file)
    nColumns = len(json.columns)
    print(nColumns)
    return nColumns


def previewData(file):
    json = pd.read_json(file)
    return json.head()


def convertToCSV(file):
    file_name = ".\\" + file_rename + ".csv"
    json = pd.read_json(file)
    csv = json.to_csv(file_name, header=True, sep=csv_delimiter)


def nestedjson2csv(file, rec_path):
    with open(file, "r") as f:
        json = jsn.loads(f.read())
        df = pd.json_normalize(json, record_path=[rec_path])
        csv = json.to_csv(".\converted.csv", header=True)


while True:
    event, values = window.read()

    file_source = values["-IN-"]
    file_rename = values["-NAME-"]
    csv_delimiter = values["-DEL-"]

    if event == "About...":
        sg.popup("Version 1.0")

    if event == "Export":
        n = countColumns(values["-IN-"])
        print(file_source)

        if n > 2:
            convertToCSV(values["-IN-"])
        sg.popup("JSON sucessfully converted to CSV")

    if event == "Preview":
        print(previewData(values["-IN-"]))
        # window["_OUTPUT_"].update(data)

    if event == sg.WIN_CLOSED or event == "Exit" or event == "Cancel":
        break
