from datetime import date, time, datetime, timedelta
import urllib.request
import json
import argparse

parser = argparse.ArgumentParser(description='Simple github punchcard')
parser.add_argument('-u', '--username', action="store", dest="username", help='github username', required=True)
args = parser.parse_args()

## Constants:
username = args.username
url_repos = 'https://api.github.com/users/%s/repos' % username


def render_table(lon):
    ## Create 'model' list: [[a, [b, c]], [a1, [b1, c1], [b2, c2]]...[an ,[bn, cn]]]
    ##                           a means day  [0, 6]
    ##                           b means hour [1, 24]
    ##                           c means commits number
    new_lst = []
    for i, s in enumerate(lon):
        new_lst.insert(i, [s[0][0], [s[0][1], s[1]]])
    model = [[0], [1], [2], [3], [4], [5], [6]]
    for i, s in enumerate(new_lst):
        model[new_lst[i][0]].append(s[1])

    ## Create dict with hour[1,24]=>screen_position[9,81]
    adict_posn = {x: y for x, y in zip(range(0, 24), range(9, 81, 3))}
    adict_days = {0: 'Mon', 1: 'Tue', 2: 'Wed', 3: 'Thu', 4: 'Fri', 5: 'Sat', 6: 'Sun'}

    ## Rename [0..6] to ['Mon'..'Sun']
    for i, s in enumerate(model):
        current_day = adict_days.get(model[i][0])
        model[i][0] = current_day

    ## Rendering:
    print("       00 01 02 03 04 05 06 07 08 09 10 11 12 13 14 15 16 17 18 19 20 21 22 23")
    print("       =======================================================================")
    for i, s in enumerate(model):
        if len(s) == 1:
            print(model[i][0])
            print("       ******************************No Commits*******************************")
            print('       -----------------------------------------------------------------------')
        if len(s) > 1:
            print(model[i][0])
            c_0 = 1
            posn = adict_posn.get(s[c_0][0])
            for val in range(len(s) - 1):
                print(('{:>%s}' % posn).format(s[c_0][1]), end=" ")
                c_0 += 1
                try:
                    posn = (adict_posn.get(s[c_0][0]) - adict_posn.get(s[c_0 - 1][0])) - 1
                except IndexError:
                    break
            print('', end='\n')
            print('       -----------------------------------------------------------------------')
    print('0. Exit')
    print('1. Menu')
    next = int(input("Enter number: "))
    if next == 0:
        exit()
    else:
        main(username)


## string -> [listof numbers]
## Consume repos name and produce list of values with days, hours and commit's counts
##     lov is list of values [[a, b], c];
##                             a is Natural[0, 6]: 0 means Monday, 1 means Tuesday ... 6 means Sunday
##                             b is Natural[0, 23]: interp. hours
##                             c is Natural[0, ...]: interp. commit's count
def punch_card(repo):
    req_comm = urllib.request.Request('https://api.github.com/repos/%s/%s/commits' % (username, repo))
    req_comm.add_header('User-Agent', 'Mozilla/5.0')
    open_req_comm = urllib.request.urlopen(req_comm)
    data_comm_raw = (open_req_comm.read().decode('utf-8'))
    json_obj = json.loads(data_comm_raw)

    newdata = []
    for i, s in enumerate(json_obj):
        comm_info = (json_obj[i]['commit']['author']).get('date')
        dt_comm_info = datetime.strptime(comm_info, "%Y-%m-%dT%H:%M:%SZ") + timedelta(hours=5)
        if dt_comm_info < datetime.now() and dt_comm_info > (datetime.now() - timedelta(days=365)):
            newdata.append([(datetime.weekday(dt_comm_info)), (datetime.time(dt_comm_info).hour)])

    newdata_2 = []
    for i, s in enumerate(newdata):
        newdata_2.insert(i, newdata.count(s))
    for i, s in enumerate(newdata):
        newdata[i] = [s, newdata_2[i]]
    lov = []
    for i in newdata:
        if i not in lov:
            lov.append(i)
    lov.sort()

    render_table(lov)


## [listof string] -> string
## Consume list of repos and produce only one
def activity(data_repo):
    lor = lst_of_repname(data_repo)
    print("0. Exit")
    for i, s in enumerate(lor):
        print(str(i + 1) + ". " + str(s))
    chosen_repo = int(input("Enter repo's number or 0 to exit: "))
    if chosen_repo == 0:
        exit()
    else:
        current_repo = lor[chosen_repo - 1]
        print('Was chosen: ' + str(current_repo))
        punch_card(current_repo)


## String - > [listof string]
## Produce filtered string with repos names (using reg ex)
##         lor means list of repos
def lst_of_repname(data_raw):
    json_obj_r = json.loads(data_raw)
    lor = []
    for i, s in enumerate(json_obj_r):
        lor.append(json_obj_r[i]['name'])
    return lor


## Username -> string
## Consume username and produce full commits data (data_repo_raw)
def main(username):
    req_rep = urllib.request.Request(url_repos)
    req_rep.add_header('User-Agent', 'Mozilla/5.0')
    open_req_rep = urllib.request.urlopen(req_rep)
    data_repo_raw = (open_req_rep.read().decode('utf-8'))

    activity(data_repo_raw)


main(username)
