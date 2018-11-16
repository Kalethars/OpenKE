f = open('../../../data/ACE17K/info/venueInfo.data', 'r')
s = f.read().split('\n')
f.close()

venueName = dict()
for line in s:
    splited = line.split()
    if len(splited) == 5:
        venueName[splited[0]] = splited[2]

f = open('WTransE2_test_venue.data', 'r')
s = f.read().split('\n')
f.close()

colorSchema = dict()
for line in s:
    splited = line.split('\t')
    if len(splited) == 6:
        colorSchema[splited[2]] = splited[3:6]

f = open('field&venue.svg', 'r')
s = str(f.read())
f.close()

f = open('WGephi_venue.data', 'w')
circles = s.split('<circle ')
for i in range(1, len(circles)):
    line = circles[i].split('/>')[0]
    cls = line.split('class="')[1].split('"')[0]
    x = line.split('cx="')[1].split('"')[0]
    y = line.split('cy="')[1].split('"')[0]
    if cls[0] == 'v':
        venue = cls[1:]
        name = venueName[venue]
        color = colorSchema[name]
        f.write('%s\t%s\t%s\t%s\t%s\t%s\n' % (x, y, name, color[0], color[1], color[2]))
f.close()
