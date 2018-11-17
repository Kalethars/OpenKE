from tkinter import *
import argparse
import math

try:
    import win_unicode_console

    win_unicode_console.enable()
except:
    pass


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


def createPoint(canvas, node, radius=3, offset=2):
    x = node[0][0]
    y = node[0][1]
    color = toHexColor(node[2])
    Canvas.create_oval(canvas, x - radius, y - radius, x + radius, y + radius, fill=color, outline=color)
    if node[3] == 'e':
        Canvas.create_text(canvas, x + radius + offset, y, text=node[1], fill=color, anchor='w')
    elif node[3] == 'w':
        Canvas.create_text(canvas, x - radius - offset, y, text=node[1], fill=color, anchor='e')
    elif node[3] == 'n':
        Canvas.create_text(canvas, x, y - radius - offset, text=node[1], fill=color, anchor='s')
    else:
        Canvas.create_text(canvas, x, y + radius + offset, text=node[1], fill=color, anchor='n')


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
    f = open('../../data/ACE17K/info/venueInfo.data', 'r')
    s = f.read().split('\n')
    f.close()

    venueCategoryId = dict()
    venueCategoryName = dict()
    for line in s:
        splited = line.split()
        if len(splited) == 5:
            venueCategoryId[splited[2]] = int(splited[4].strip())
            venueCategoryName[splited[2]] = splited[3].replace('.', ' ')

    categories = sorted(set(venueCategoryId.values()))
    for i in range(len(categories)):
        for node in nodes:
            if venueCategoryId[node[1]] == categories[i]:
                categoryName = venueCategoryName[node[1]]
                color = toHexColor(node[2])
                x = 20
                y = 20 + i * 20
                Canvas.create_oval(canvas, x - radius, y - radius, x + radius, y + radius, fill=color, outline=color)
                Canvas.create_text(canvas, x + radius + offset, y, text=categoryName, fill=color, anchor='w')
                break


parser = argparse.ArgumentParser()
parser.add_argument('--method', type=str, required=False)
parser.add_argument('--target', type=str, required=False)
parser.add_argument('--manual', type=str, required=False)
parser.add_argument('--x', type=int, required=False)
parser.add_argument('--y', type=int, required=False)
parsedArgs = parser.parse_args()

method = parsedArgs.method if parsedArgs.method else 'WTransE2_test'
target = parsedArgs.target if parsedArgs.target else 'venue'
manual = parsedArgs.manual
sizeX = parsedArgs.x if parsedArgs.x else 900
sizeY = parsedArgs.y if parsedArgs.y else 900

manualNode = dict()
if not manual is None:
    splited = manual.split(',')
    for each in splited:
        manualNode[each.split(':')[0].lower()] = each.split(':')[1]

f = open('./data/%s_%s.data' % (method, target), 'r')
s = f.read().split('\n')
f.close()

nodes = []
for line in s:
    splited = line.split('\t')
    if len(splited) == 6:
        # Coordinate, Label, Color
        nodes.append([[float(splited[0]), float(splited[1])],
                      splited[2],
                      (float(splited[3]), float(splited[4]), float(splited[5]))])
normalize(nodes, 1050 - sizeX, 1050, 950 - sizeY, 950)
nodeNum = len(nodes)

distance = [[0] * nodeNum for i in range(nodeNum)]
nearest = []
for i in range(nodeNum):
    for j in range(nodeNum):
        distance[i][j] = calcDistance(nodes[i], nodes[j])
    nearest.append(sorted([j for j in range(i)] + [j for j in range(i + 1, nodeNum)], key=lambda x: distance[i][x]))

for i in range(nodeNum):
    bestAnchor = {'e', 's', 'n', 'w'}
    for j in nearest[i]:
        directions = getDirection(nodes[i], nodes[j])
        if distance[i][j] > 50:
            break
        if j < i:
            if nodes[j][3] in {'n', 's'}:
                bestAnchor.discard(nodes[j][3])
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
            nodes[i].append(anchor)
            break
    # print(i, nodes[i], nearest[i][:5], [getDirection(nodes[i], nodes[j]) for j in nearest[i][:5]], bestAnchor)

if len(manualNode) > 0:
    for node in nodes:
        if manualNode.get(node[1].lower(), 0) != 0:
            node[3] = manualNode[node[1].lower()]

window = Tk()
window.title('%s graph of %s' % (target.capitalize(), method))
canvas = Canvas(window, height=1000, width=1200, bg='white')
for node in nodes:
    createPoint(canvas, node)

if target == 'venue':
    venueLegend(canvas, nodes)

canvas.pack()
window.mainloop()
