from collections import OrderedDict
import json
from datetime import date

hist = OrderedDict(json.load(open("../../__atomic_gitter_logs/lumixLog.txt", 'r')))
data = []
users = []

sucks = 0
sucksdict = {}

for key in hist:
    log = hist[key]

    usr = log['user']
    dat = log['date']
    msg = log['html']

    if usr not in users:
        users.append(usr)


#suckylogic

    if usr not in sucksdict:
        sucksdict[usr] = 0;


    sucksinmsg = msg.lower().count("sux")+msg.lower().count("suck");
    sucksdict[usr] += sucksinmsg;
    sucks += sucksinmsg;





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



sucks_scores = sorted(sucksdict.items(), key=lambda x: x[1], reverse=True);
sucksstr = "TOTAL SUCKS GIVEN: "+str(sucks)
sucksstr += "<br><br>TOP SCORES:"
sucksstr += "<table class=\"sux\">"
c=0;
for entry in sucks_scores:
    sucksstr += "<tr><td>"+entry[0]+"</td><td>"+str(entry[1])+"</td></tr>"
    c+=1;
    if c>=8:
        break
sucksstr += "</table>"

open("index.html", 'w').write(open("template.html", 'r').read()
                              .replace("[SHITGOESHERE]", 'Messages: {}, Users: {}, Updated: {}'.format(len(data),len(users),str(date.today())))
                              .replace("[USERSGOESHERE]", users_str)
                              .replace("[SUCKSCOUNTER]", sucksstr)
                              .replace("[SIZEGOESHERE]", '{:.2f}'.format((len(json.dumps(data).encode())/1000000)/4.75)) #approx zip compression
                              )

