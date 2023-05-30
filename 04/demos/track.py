import json

personlasttime: dict = {}

with open("people.json", "r", encoding="utf-8") as f:
    nullcount = 0
    tracking = json.load(f)
    allitems = tracking["Persons"]
    for item in allitems:
        person = item["Person"]
        timestamp = item["Timestamp"]
        try:
            face = person["Face"]
            confidence = float(face["Confidence"])
            index = int(person["Index"])
            if confidence > 10.0:
                try:
                    lasttime = personlasttime[index]
                    if lasttime < 0:
                        print(f"person {index} appears at {timestamp}")
                        personlasttime[index] = timestamp
                except ValueError:
                    personlasttime[index] = timestamp
                    print(f"person {index} appears at {timestamp}")
        except ValueError:
            nullcount += 1
        for personindex, stamp in personlasttime.items():
            if stamp > 0 and (timestamp - stamp) > 1000:
                print(f"person {personindex} leaves at {timestamp}")
                personlasttime[personindex] = -100
