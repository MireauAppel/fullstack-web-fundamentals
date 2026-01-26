import webbrowser
import os
html_output = """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Prototype meteo.data</title>
    <style>
        table{
            border-collapse:collapse;
            width:100%
        }
        td,th{
            border: 1px solid black;
            padding: 8px;
        }
        .very-cold{
            background-color:DodgerBlue
        }
        .cold{
            background-color:LimeGreen
        }
        .warm{
            background-color:Gold
        }
        .hot{
            background-color:Orange
        }
        .very-hot{
            background-color:OrangeRed
        }
    </style>
</head>
<body>
    <h1>Table of all meteor.data</h1>
    <table>
        <tr>
            <th>Année</th>
            <td>J</td>
            <td>F</td>
            <td>M</td>
            <td>A</td>
            <td>M</td>
            <td>J</td>
            <td>J</td>
            <td>A</td>
            <td>S</td>
            <td>O</td>
            <td>N</td>
            <td>D</td>
        </tr>
"""

try:
    with open(r"/amuhome/a24007103/Documents/L2/S4/web/TP1.2/meteo.data", "r") as file:
        for line in file:
            data = line.strip().split()
            year=data[0]
            temp=int(data[2])
            if int(data[1]) == 1:
                html_output+="        <tr>\n"
                html_output+= f"            <td>{year}</td>\n"
            if(temp<=0):
                html_output+= f"            <td class='very-cold'>{temp}</td>\n"
            if(0<temp<=10):
                html_output+= f"            <td class='cold'>{temp}</td>\n"
            if(10<temp<=20):
                html_output+= f"            <td class='warm'>{temp}</td>\n"
            if(20<temp<=30):
                html_output+= f"            <td class='hot'>{temp}</td>\n"
            if(30<temp<=40):
                html_output+= f"            <td class='very-hot'>{temp}</td>\n"
            if data[1] == 12:
                html_output+="        </tr>\n"
except FileNotFoundError:
    print("Erreur: Le fichier meteo.data est introuvable.")
html_output+= """
</table>
</body>
</html>
"""
print(html_output)

file_name = "meteo.data_table"

with open(file_name, "w", encoding="utf-8") as f:
    f.write(html_output)
complete_path="file://"+os.path.realpath(file_name)
webbrowser.open(complete_path)
