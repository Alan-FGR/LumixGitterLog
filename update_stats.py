import json
from collections import OrderedDict

hist = OrderedDict(json.load(open("../../__atomic_gitter_logs/lumixLog.txt", 'r')))

counters = {
    "sucks":["sux", "suck"],
    "jesus":["gees","jees","geez","jeez","jesu","gesu","jebu","sheesh"],
    "shit":["shit","crap"],
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




#PLOTTING
from matplotlib import pyplot as plt; import numpy as np; import matplotlib.patches as mpatches
from itertools import islice; import copy

def GetPlottableVals(num):
    top_scores = OrderedDict(sorted(copy.deepcopy(scores).items(), key=lambda item: item[1]['total'], reverse=True))
    top_scores = OrderedDict(islice(top_scores.items(), num))

    # SHIIIIIIIIIIIITTTTTTTTTTTT
    for user, score in top_scores.items():
        score.pop('total')
        # END SHIIIIIIIIIIIITTTTTTTTTTTT

    return (num,top_scores, np.array([[v for n,v in scr.items()] for usr,scr in top_scores.items()]))



default_cols = plt.rcParams['axes.color_cycle']

patches = []
cc=0
for c in counters:
    patches.append(mpatches.Patch(label=c, color=default_cols[cc]))
    cc+=1

#pie
num_users,top_scores,vals = GetPlottableVals(5)

fig, ax = plt.subplots(figsize=(4, 4))
ax.pie(vals.flatten(), radius=1.2,
       colors=plt.rcParams["axes.prop_cycle"].by_key()["color"][:vals.shape[1]])
ax.pie(vals.sum(axis=1), radius=1, labels=[name for name in top_scores],
       colors = [[x/num_users/2+0.5]*3 for x in range(num_users)]
       )
ax.set(aspect="equal", title='TOP '+str(num_users)+' PIE CHART')

plt.legend(handles=patches, loc="center")

plt.savefig('piechart.png', bbox_inches='tight')

#//bar

num_users,top_scores,vals = GetPlottableVals(12)

fig, ax = plt.subplots(figsize=(8, 4))
plt.subplots_adjust(left=0.07, right=0.95, top=0.9, bottom=0.2)
bar_locations = np.arange(num_users)
last_vals = [100]*num_users

ax.set_xticks([x for x in range(num_users)])
ax.set_xticklabels([name for name in sorted_scores], rotation=-30, ha="left")
ax.set(title='TOP '+str(num_users)+' BARS')

for score in range(4):
    ax.bar(bar_locations, [v[score] for v in vals], bottom=last_vals, color=default_cols[score])
    for user in range(num_users):
        last_vals[user] += vals[user][score]

plt.legend(handles=patches)
# plt.show()
plt.savefig('plot.png', bbox_inches='tight')
#END PLOTTING




totalscores = {ctr:0 for ctr in counters}
totalscores['total']=0
for user,score in scores.items():
    for name,value in score.items():
        totalscores[name] += value;
sorted_scores["<b>TOTALS</b>"] = totalscores
sorted_scores.move_to_end("<b>TOTALS</b>", last=False)

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

html += '<img src="piechart.png"><img src="plot.png">'

html += "<table><tr><th>User</th>"

for counter in counters:
    html += "<th><b>"+counter+"</b></th>" # headers

html += "<th><b>SCORE</b></th>"

html += "</tr>"

for user, scores in sorted_scores.items():
    html += "<tr><td><b>" + user + "</b></td>"
    for score, value in scores.items():
        html += "<td>" + str(value) + "</td>"
    html += "</tr>"

html += "</table></body></html>"


#print(html)
open("stats.html", 'w').write(html);