import json as jsn
from PySimpleGUI.PySimpleGUI import popup_error
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
        sg.Text("Delimiter: "),
        sg.Input(default_text=",", size=(3, 1), key="-DEL-"),
        sg.Text("Encoding: "),
        sg.Input(default_text="UTF8", size=(5, 1), key="-ENC-"),
    ],
    [
        sg.Text("Choosen file source: "),
        sg.Input(),
        sg.FileBrowse(key="-IN-", file_types=(("JSON Files", "*.json"),)),
    ],
    [sg.Text("Converted File name: "), sg.Input(key="-NAME-"), sg.Text(".csv")],
    [sg.Text("Data preview"), sg.Multiline(size=(45, 5), key="_OUTPUT_")],
    [sg.Button("Preview"), sg.Button("Export"), sg.Button("Cancel")],
]

#  Building Main Window
window = sg.Window("JSON2CSV Converter", layout, icon=icon_src, size=(600, 300))


def countColumns(file):
    json = pd.read_json(file)
    nColumns = len(json.columns)
    return nColumns


def previewData(file):
    if countColumns(file) > 2:
        json = pd.read_json(file)
    else:
        with open(file, "r") as f:
            file_name = ".\\" + file_rename + ".csv"
            data = jsn.loads(f.read())
            json = pd.json_normalize(data, getNestedColumn(file_source))
    return json


def getNestedColumn(file):
    json = pd.read_json(file)
    columns = list(json.columns)
    return columns[1]


def convertToCSV(file):
    file_name = ".\\" + file_rename + ".csv"
    json = pd.read_json(file)
    csv = json.to_csv(file_name, header=True, sep=csv_delimiter)


def nestedjson2csv(file, rec_path):
    with open(file, "r") as f:
        file_name = ".\\" + file_rename + ".csv"
        json = jsn.loads(f.read())
        df = pd.json_normalize(json, record_path=[rec_path])
        csv = df.to_csv(file_name, header=True, sep=csv_delimiter)


def previewWindow(data):  # build another window to display the data preview
    layout = [[sg.Text(data)]]
    window = sg.Window("Data Preview", layout, size=(600, 300))
    event, values = window.read()
    while True:
        if event == "Exit" or event == sg.WIN_CLOSED:
            break

    window.close()


while True:
    event, values = window.read()

    file_source = values["-IN-"]
    file_rename = values["-NAME-"]
    csv_delimiter = values["-DEL-"]

    if event == "About...":
        sg.popup("Version 1.0")

    if event == "Export":
        n = countColumns(file_source)
        print(file_source)

        if n > 2:
            convertToCSV(file_source)
        elif n <= 2:
            nestedjson2csv(file_source, getNestedColumn(file_source))

        sg.popup("JSON sucessfully converted to CSV")

    if event == "Preview":
        previewWindow(previewData(file_source))

    if event == sg.WIN_CLOSED or event == "Exit" or event == "Cancel":
        break