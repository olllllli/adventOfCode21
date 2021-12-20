import json
from datetime import datetime

data = {}
with open("data.json") as f:
    data = json.load(f)

for member in sorted(data["members"].keys(), key=lambda m: data["members"][m]["local_score"], reverse=True):
    memData = data["members"][member]
    print("member: {:<30} stars: {:2d}, score: {}".format(memData["name"] or member, memData["stars"], memData["local_score"]))

    # print day data
    for day in sorted(memData["completion_day_level"].keys(), key=lambda n: int(n)):
        dayData = memData["completion_day_level"][day]
        p1 = dayData.get("1")["get_star_ts"]
        p2 = (dayData.get("2") or {}).get("get_star_ts")
        p1Date = datetime.fromtimestamp(int(p1)).strftime("%H:%M:%S %Y-%m-%d")
        p2Date = "" if not p2 else datetime.fromtimestamp(int(p2)).strftime("%H:%M:%S %Y-%m-%d")
        print("   Day {:>2}:   {:>21}   {:>21}".format(day, p1Date, p2Date))

    print("")