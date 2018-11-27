from tkinter import *
import argparse

try:
    import win_unicode_console

    win_unicode_console.enable()
except:
    pass


def getDefaultRadius(target):
    if target in {'venue'}:
        return 3
    else:
        return 1.5


def calcDistance(node1, node2):
    return ((node1[0][0] - node2[0][0]) ** 2 + (node1[0][1] - node2[0][1]) ** 2) ** 0.5


def getDirection(node1, node2, threshold=20):
    dx = node2[0][0] - node1[0][0]
    dy = node2[0][1] - node1[0][1]
    distance = calcDistance(node1, node2)
    directions = set()
    if dx == 0:
        if dy > 0:
            directions.add('n')
        else:
            directions.add('s')
    elif dx > 0:
        if distance < threshold:
            directions.add('e')
        if dy >= dx:
            directions.add('s')
        elif dx > dy > -dx:
            directions.add('e')
        else:
            directions.add('n')
    else:
        if distance < threshold:
            directions.add('w')
        if dy <= dx:
            directions.add('n')
        elif -dx > dy > dx:
            directions.add('w')
        else:
            directions.add('s')
    return directions


def toHex(value):
    hexValue = str(hex(round(value * 255)))[2:].upper()
    return '0' * (2 - len(hexValue)) + hexValue


def toHexColor(color):
    return '#%s%s%s' % (toHex(color[0]), toHex(color[1]), toHex(color[2]))


def createPoint(canvas, node, radius=3):
    x = node[0][0]
    y = node[0][1]
    color = node[2]
    Canvas.create_oval(canvas, x - radius, y - radius, x + radius, y + radius, fill=color, outline=color)


def createLabel(canvas, label, radius=3, offset=2, noColor=False):
    x = label[0][0]
    y = label[0][1]
    text = label[1]
    color = '#000000' if noColor else label[2]
    anchor = label[3]

    if anchor == 'e':
        Canvas.create_text(canvas, x + radius + offset, y, text=text, fill=color, anchor='w')
    elif anchor == 'w':
        Canvas.create_text(canvas, x - radius - offset, y, text=text, fill=color, anchor='e')
    elif anchor == 'n':
        Canvas.create_text(canvas, x, y - radius - offset, text=text, fill=color, anchor='s')
    elif anchor == 's':
        Canvas.create_text(canvas, x, y + radius + offset, text=text, fill=color, anchor='n')
    else:
        Canvas.create_text(canvas, x, y, text=text, fill=color)


def normalize(nodes, lowX=150, highX=1050, lowY=50, highY=950):
    minX = nodes[0][0][0]
    maxX = nodes[0][0][0]
    minY = nodes[0][0][1]
    maxY = nodes[0][0][1]
    for node in nodes:
        minX = min(minX, node[0][0])
        maxX = max(maxX, node[0][0])
        minY = min(minY, node[0][1])
        maxY = max(maxY, node[0][1])
    for node in nodes:
        node[0][0] = (node[0][0] - minX) / (maxX - minX) * (highX - lowX) + lowX
        node[0][1] = (node[0][1] - minY) / (maxY - minY) * (highY - lowY) + lowY


def venueLegend(canvas, nodes, radius=3, offset=2):
    f = open('./data/venue_color.data', 'r')
    s = f.read().split('\n')
    f.close()

    cnt = 0
    colorIndex = dict()
    for line in s:
        splited = line.split()
        if len(splited) == 4:
            categoryName = splited[0].replace('.', ' ')
            color = toHexColor(list(map(lambda x: float(x), splited[1:])))
            colorIndex[color] = '\n/'.join(categoryName.split('/'))
            x = 20
            y = 20 + cnt * 20
            Canvas.create_oval(canvas, x - radius, y - radius, x + radius, y + radius, fill=color, outline=color)
            Canvas.create_text(canvas, x + radius + offset, y, text=categoryName, fill=color, anchor='w')

            cnt += 1


def computeCore(points):
    points = sorted(points)
    return points[int(len(points) / 2)]


parser = argparse.ArgumentParser()
parser.add_argument('--method', type=str, required=False)
parser.add_argument('--target', type=str, required=False)
parser.add_argument('--manual', type=str, required=False)
parser.add_argument('--x', type=int, required=False)
parser.add_argument('--y', type=int, required=False)
parser.add_argument('--r', type=float, required=False)
parsedArgs = parser.parse_args()

method = parsedArgs.method if parsedArgs.method else 'WTransE2_test'
target = parsedArgs.target.lower() if parsedArgs.target else 'venue'
manual = parsedArgs.manual
sizeX = parsedArgs.x if parsedArgs.x else 900
sizeY = parsedArgs.y if parsedArgs.y else 900
radius = parsedArgs.r if parsedArgs.r else getDefaultRadius(target)

showLabel = True if target in {'venue'} else False

manualNode = dict()
if not manual is None:
    splited = manual.split(',')
    for each in splited:
        manualNode[each.split(':')[0].lower()] = each.split(':')[1]

f = open('./data/%s_%s.data' % (method, target), 'r')
s = f.read().split('\n')
f.close()

nodes = []
colors = dict()
for line in s:
    splited = line.split('\t')
    if len(splited) >= 6:
        # Coordinate, Label, Color
        coordinate = [float(splited[0]), float(splited[1])]
        label = splited[2]
        color = toHexColor((float(splited[3]), float(splited[4]), float(splited[5])))
        nodes.append([coordinate, label, color])
        colors[label] = color
normalize(nodes, 1150 - sizeX, 1150, 950 - sizeY, 950)
nodeNum = len(nodes)

pointX = dict()
pointY = dict()
for node in nodes:
    label = node[1]
    if not label in pointX:
        pointX[label] = []
        pointY[label] = []
    pointX[label].append(node[0][0])
    pointY[label].append(node[0][1])

labels = []
for label in pointX.keys():
    coreX = computeCore(pointX[label])
    coreY = computeCore(pointY[label])
    labels.append([[coreX, coreY], label, colors[label]])
labelNum = len(labels)

distance = [[0] * labelNum for i in range(labelNum)]
nearest = []
for i in range(labelNum):
    for j in range(labelNum):
        distance[i][j] = calcDistance(labels[i], labels[j])
    nearest.append(sorted([j for j in range(i)] + [j for j in range(i + 1, labelNum)], key=lambda x: distance[i][x]))

for i in range(labelNum):
    if target in {'venue'}:
        bestAnchor = {'e', 's', 'n', 'w'}
        for j in nearest[i]:
            directions = getDirection(labels[i], labels[j])
            if distance[i][j] > 50:
                break
            if j < i:
                if labels[j][3] in {'n', 's'}:
                    bestAnchor.discard(labels[j][3])
            finished = False if len(bestAnchor) > 1 else True
            for direction in directions:
                if finished:
                    break
                bestAnchor.discard(direction)
                if len(bestAnchor) == 1:
                    finished = True
            if finished:
                break
        for anchor in ['e', 'w', 'n', 's']:
            if anchor in bestAnchor:
                labels[i].append(anchor)
                break
    else:
        labels[i].append('c')

if len(manualNode) > 0:
    for label in labels:
        if manualNode.get(label[1].lower(), 0) != 0:
            label[3] = manualNode[label[1].lower()]

window = Tk()
window.title('%s graph of %s' % (target.capitalize(), method))
canvas = Canvas(window, height=1000, width=1300, bg='white')

for node in nodes:
    createPoint(canvas, node, radius)

for label in labels:
    createLabel(canvas, label, radius, noColor=False if target in {'venue'} else True)

if target in {'venue', 'paper'}:
    venueLegend(canvas, nodes)

canvas.pack()
window.mainloop()
