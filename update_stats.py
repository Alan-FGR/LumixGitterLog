import json
from collections import OrderedDict

hist = OrderedDict(json.load(open("../../__atomic_gitter_logs/lumixLog.txt", 'r')))

counters = {
    "suck":["sux", "suck"],
    "jesus":["gees","jees","geez","jeez","jesu","gesu","jebu"],
    "shit":["shit","sheesh","crap"],
    "trollface":["trollface"]
}

scores = {}

for key in hist:
    log = hist[key]
    usr = log['user']
    msg = log['html']

    if usr not in scores:
        scores[usr] = {}
        scores[usr] = dict.fromkeys(counters.keys(),0)
        scores[usr]["total"] = 0

    for counter, matchergroup in counters.items():
        for matcher in matchergroup:
            c = msg.lower().count(matcher)
            scores[usr][counter] += c
            scores[usr]["total"] += c

sorted_scores = OrderedDict(sorted(scores.items(), key=lambda item: item[1]['total'], reverse=True))

html = """
<html>
<head>
<style>
table {
    border-collapse: collapse;
}

th, td {
    text-align: right;
    padding: 10px;
    border: 1px solid #ddd;
}

tr:nth-child(even){background-color: #eee}

th {
    background-color: #0a0;
    color: white;
}
</style>
</head>
<body>
"""

html += "<table><tr><th>User</th>"

for counter in counters:
    html += "<th><b>"+counter+"</b></th>" # headers

html += "<th><b>TOTAL</b></th>"

html += "</tr>"

for user, scores in sorted_scores.items():
    html += "<tr><td><b>" + user + "</b></td>"
    for score, value in scores.items():
        html += "<td>" + str(value) + "</td>"
    html += "</tr>"

html += "</table></body></html>"


print(html)
open("stats.html", 'w').write(html);