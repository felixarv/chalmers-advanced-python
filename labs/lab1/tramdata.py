import json
from pprint import pprint
from haversine import haversine


TRAM_STOP_FILE = 'labs/data/tramstops.json'
with open(TRAM_STOP_FILE, 'r') as fromFile:
    data = json.load(fromFile)

with open("labs/data/tramnetwork.json", "r") as jsonfile:
    tramdict = json.load(jsonfile)


with open ("labs/data/tramlines.txt", "r", encoding= "UTF-8") as file:
    lines = file.read().replace(":","").strip().split("\n\n")
    lines = [line.split("\n") for line in lines]

    

def build_tram_stops(jsonobject):

    stopdict = {x: {"lat":jsonobject[x]['position'][0], "lon":jsonobject[x]['position'][1]} for x in jsonobject}

    return stopdict


def build_tram_lines(lines):

    linedict = {}
    timedict = {}

    for line in lines:
        values=[]
        key = line[0]
        for i in range(1, len(line) - 1):
            name, time = [item.strip() for item in line[i].split("  ") if item]
            next_name, next_time = [item.strip() for item in line[i+1].split("  ") if item]
            time_diff = int(next_time) - int(time)
            values.append(name)
            if name not in timedict:
                timedict[name] = {}
            if next_name not in timedict:
                timedict[next_name] = {}
            if name not in timedict[next_name]:
                timedict[name][next_name] = time_diff
        values.append(next_name)
        linedict[key] = values
    
    return (linedict, timedict)
def build_tram_network(stopfile, linefile):

    outdict = {"stops": build_tram_stops(stopfile), "lines": build_tram_lines(linefile)[0], "times": build_tram_lines(linefile)[1]}


    with open("labs/data/tramnetwork.json", "w") as file:
        json.dump(outdict, file)


def lines_via_stop(linedict, stop):

    return [key for key in linedict if stop in linedict[key]]


def lines_between_stops(linedict, stop1, stop2):

    return [key for key in linedict if stop1 in linedict[key] and stop2 in linedict[key]]



def time_between_stops(linedict, timedict, line, stop1, stop2):
       
       
    if linedict[str(line)].index(stop1) < linedict[str(line)].index(stop2):
        index_1 = linedict[str(line)].index(stop1)
        index_2 = linedict[str(line)].index(stop2) + 1
    else:
        index_1 = linedict[str(line)].index(stop2)
        index_2 = linedict[str(line)].index(stop1) + 1

    stoplist = linedict[str(line)][index_1:index_2]

    time = 0
    for i in range(len(stoplist) - 1):
        if stoplist[i+1] in timedict[stoplist[i]]:
            time += timedict[stoplist[i]][stoplist[i+1]]
            
        elif stoplist[i] in timedict[stoplist[i+1]]:
            time += timedict[stoplist[i+1]][stoplist[i]]

    return time
       

def distance_between_stops(stopdict, stop1, stop2):
    loc_1 = (float(stopdict[stop1]["lat"]),float(stopdict[stop1]["lon"]))
    loc_2 = (float(stopdict[stop2]["lat"]),float(stopdict[stop2]["lon"]))
    
    return haversine(loc_1, loc_2)


def answer_query(tramdict, query):

    if query[0] == "Via":
        if len(query) == 3: 
            return lines_via_stop(dict(tramdict["lines"]), " ".join(query[1:]))
        elif query[0] == "Via":
            return lines_via_stop(tramdict["lines"], query[1])

    if query[0] == "Between":
        if len(query) == 5:
            if query[3] == "And": 
                return lines_between_stops(tramdict["lines"], " ".join(query[1:3]), query[4])   
            elif query[2] == "And":
                return lines_between_stops(tramdict["lines"], query[1], " ".join(query[3:]))
        elif len(query) == 4:
            return lines_between_stops(tramdict["lines"], query[1], query[3])
    
    if query[0] == "Time":
        if len(query) == 9:
            return time_between_stops(tramdict["lines"], tramdict["times"], int(query[2]), " ".join(query[4:6]), " ".join(query[7:]))
        elif len(query) == 8 and query[5] == "To":
            return time_between_stops(tramdict["lines"], tramdict["times"], int(query[2]), query[4], " ".join(query[6:]))
        elif len(query) == 8:
            return time_between_stops(tramdict["lines"], tramdict["times"], int(query[2]), " ".join(query[4:6]), query[7])
        elif len(query) == 7:
            return time_between_stops(tramdict["lines"], tramdict["times"], int(query[2]), query[4], query[6])
        
    if query[0] == "Distance":
        if len(query) == 7:
            return distance_between_stops(tramdict["stops"], " ".join(query[2:4]), " ".join(query[5:]))
        elif len(query) == 6 and query[3] == "To":
            return distance_between_stops(tramdict["stops"], query[2], " ".join(query[4:]))
        elif len(query) == 6:
            return distance_between_stops(tramdict["stops"], " ".join(query[2:4]), query[5])
        elif len(query) == 5:
            return distance_between_stops(tramdict["stops"], query[2], query[4])
            
    return "sorry, try again"


def dialogue(tramfile):
    with open(tramfile, "r") as file:
        tramdict = json.load(file)


    while True:
        try:
            print("Choose option:\n via <stop>\n between <stop1> and <top2\n time with <line> from <stop1> to <top2>\n distance from <stop1> to <top2>\n quit")
            query = input("").lower().title().split()
            if query[0] == "Quit":
                break
            answer = answer_query(tramdict, query)

            if answer:
                print(answer)
                print(bool(answer))
            else: 
                print("unknown arguments")
                print(bool(answer))
        except:
            print("sorry, try that again")

            
        
        
          
            
        
   

dialogue("labs/data/tramnetwork.json")

    
   
    
