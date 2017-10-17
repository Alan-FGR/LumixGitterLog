from collections import OrderedDict
import json
from datetime import date

hist = OrderedDict(json.load(open("../../__atomic_gitter_logs/lumixLog.txt", 'r')))
data = []
users = []

sucks = 0

for key in hist:
    log = hist[key]

    usr = log['user']
    dat = log['date']
    msg = log['html']

    if usr not in users:
        users.append(usr)

    sucks+=msg.count("suck")
    sucks+=msg.count("sux")

    # TODO UNCOMMENT WHEN YOU CAN MAKE LAZY LOADER WORK :(
    # if ("<img" in log['html']):
    #     msg = msg.replace('src=', 'src="loading.PNG" data-src=')

    dat = dat[:10] + "<br>" + dat[11:19]

    data.append({
        'user': usr,
        'date': dat,
        'html': msg
    })

open("log.json", 'w').write(json.dumps(data))  # , indent=2))

users.sort()
users.insert(0,"All")
users_str = ""
for u in users:
    users_str+='<option value="{}">{}</option>\n'.format(u,u)

open("index.html", 'w').write(open("template.html", 'r').read()
                              .replace("[SHITGOESHERE]", 'Messages: {}, Users: {}, Updated: {}'.format(len(data),len(users),str(date.today())))
                              .replace("[USERSGOESHERE]", users_str)
                              .replace("[SUCKSCOUNTER]", str(sucks))
                              .replace("[SIZEGOESHERE]", '{:.2f}'.format((len(json.dumps(data).encode())/1000000)/4.75)) #approx zip compression
                              )
