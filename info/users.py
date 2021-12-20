import json

data = {}
with open("data.json") as f:
    data = json.load(f)

for member in sorted(data["members"].keys(), key=lambda m: data["members"][m]["local_score"], reverse=True):
    memData = data["members"][member]
    print("member: {:<30} stars: {:2d}, score: {}".format(memData["name"] or member, memData["stars"], memData["local_score"]))