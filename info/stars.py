import json
from datetime import datetime, timedelta

def deltaToStr(delta: timedelta):
    if delta.days > 0:
        return ">24h"

    res = ""
    hours = delta.seconds // 60 // 60
    minutes = (delta.seconds % (60 * 60)) // 60
    seconds = delta.seconds % 60

    res += f"{seconds:2d}s"
    if hours > 0:
        res = f"{hours:2d}h {minutes:2d}m " + res
    else:
        res = f"{minutes:2d}m " + res

    return res

data = {}
with open("data.json") as f:
    data = json.load(f)

stars = {}
for i in range(25):
    stars[str(i + 1)] = {"1": [], "2": [], "happened": False}

for member in data["members"]:
    memData = data["members"][member]
    name = memData["name"] or member

    # get each members days
    for day in memData["completion_day_level"]:
        dayData = memData["completion_day_level"][day]
        p1 = dayData.get("1")["get_star_ts"]
        p2 = (dayData.get("2") or {}).get("get_star_ts")
        stars[day]["1"].append((memData["name"] or "(#"+member+")", p1))
        stars[day]["2"].append((memData["name"] or "(#"+member+")", p2))
        stars[day]["happened"] = True

for day in stars:
    released = datetime.fromisoformat("2021-12-{:02d}#16:00:00".format(int(day)))
    if stars[day]["happened"] == False:
        continue
    
    print(f"Day {day:>2}:       Part 1                                      Part 2")

    p1 = sorted(stars[day]["1"], key=lambda m: m[1] or 100000000000000000000)
    p2 = sorted(stars[day]["2"], key=lambda m: m[1] or 100000000000000000000)

    for i in range(len(p1)):
        p1time = deltaToStr(datetime.fromtimestamp(int(p1[i][1])) - released)
        # display the row
        if not p2[i][1]:
            print("        {:>12}  {:<30}".format(p1time, p1[i][0]))
        else:
            p2time = deltaToStr(datetime.fromtimestamp(int(p2[i][1])) - released)
            print("        {:>12}  {:<30} {:>11}  {:<30}".format(p1time, p1[i][0], p2time, p2[i][0]))

    print()
