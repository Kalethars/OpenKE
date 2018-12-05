f = open('../../../data/ACE17K/info/venueInfo.data', 'r')
s = f.read().split('\n')
f.close()

venueName = dict()
venueCategory = dict()
for line in s:
    splited = line.split()
    if len(splited) == 5:
        venueName[splited[0]] = splited[2]
        venueCategory[splited[0]] = splited[3]

f = open('../../../benchmarks/ACE17K/triplets.txt', 'r')
s = f.read().split('\n')
f.close()

paperVenue = dict()
for line in s:
    splited = line.split()
    if len(splited) == 3:
        if splited[1] == '4':
            paperVenue[splited[0][1:]] = splited[2][1:]

f = open('venue_color.data', 'r')
s = f.read().split('\n')
f.close()

colorSchema = dict()
for line in s:
    splited = line.split()
    if len(splited) == 4:
        colorSchema[splited[0]] = splited[1:]

f = open('paper.svg', 'r')
s = str(f.read())
f.close()

f = open('WGephi_paper.data', 'w')
circles = s.split('<circle ')
for i in range(1, len(circles)):
    line = circles[i].split('/>')[0]
    cls = line.split('class="')[1].split('"')[0]
    x = line.split('cx="')[1].split('"')[0]
    y = line.split('cy="')[1].split('"')[0]
    if cls[0] == 'p':
        paper = cls[1:]
        try:
            venue = paperVenue[paper]
        except:
            continue
        name = venueName[venue]
        color = colorSchema[venueCategory[venue]]
        f.write('%s\t%s\t%s\t%s\t%s\t%s\n' % (x, y, name, color[0], color[1], color[2]))
f.close()
