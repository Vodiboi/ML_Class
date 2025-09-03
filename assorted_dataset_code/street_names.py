# process british and bay area street names
f_in = "bay_area.txt"
f_out = "bay_area_processed.txt"

with open(f_in, "r") as f:
    lines = f.read().splitlines()

l2 = []
seen = set()
for l in lines:
    b = 1
    for j in l:
        if (not ('a' <= j and j <= 'z') and not ('A' <= j and j <= 'Z') and (j != ' ')):
            b = 0
            break
    if b:
        s = l.lower().replace(" ", "_")
        if s not in seen:
            l2.append(s)
            seen.add(s)


with open(f_out, "w") as f:
    print(*l2, sep='\n', file=f)