from tkinter import *
import numpy as np
import argparse

try:
    import win_unicode_console

    win_unicode_console.enable()
except:
    pass


def getDefaultDotRadius(target):
    if target in {'venue'}:
        return 3
    else:
        return 1.5


def calcDistance(node1, node2):
    return abs(node1[0] - node2[0])


def getDirection(node1, node2, threshold=20):
    dx = node2[0].real - node1[0].real
    dy = node2[0].imag - node1[0].imag
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
    x = node[0].real
    y = node[0].imag
    color = node[2]
    Canvas.create_oval(canvas, x - radius, y - radius, x + radius, y + radius, fill=color, outline=color)


def createLabel(canvas, label, radius=3, offset=2, noColor=False):
    x = label[0].real
    y = label[0].imag
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


def normalize(nodes, centerX=600, centerY=500, std=200):
    nodeX = np.array([node[0].real for node in nodes])
    nodeY = np.array([node[0].imag for node in nodes])
    nodeX = (nodeX - np.average(nodeX)) / np.std(nodeX)
    nodeY = (nodeY - np.average(nodeY)) / np.std(nodeY)
    nodeX = nodeX * std + centerX
    nodeY = nodeY * std + centerY
    for i in range(len(nodes)):
        nodes[i][0] = complex(nodeX[i], nodeY[i])


def venueLegend(canvas, radius=3, offset=5, split=False):
    if method.count('_') >= 2:
        f = open('./data/venue_%s_color.data' % (method.split('_')[-1].upper()), 'r')
    else:
        f = open('./data/venue_color.data', 'r')
    s = f.read().split('\n')
    f.close()

    x = 20
    y = 20
    for line in s:
        splited = line.split()
        if len(splited) == 4:
            categoryName = splited[0].replace('.', ' ')
            if split:
                categoryName = categoryName.split('/')
            else:
                categoryName = [categoryName]
            color = toHexColor(list(map(lambda x: float(x), splited[1:])))
            Canvas.create_oval(canvas, x - radius, y - radius, x + radius, y + radius, fill=color, outline=color)
            for i in range(len(categoryName)):
                Canvas.create_text(canvas, x + radius + offset, y, text=categoryName[i], fill=color, anchor='w')
                y += 20


def computeCore(pointX, pointY):
    distances = []
    num = len(pointX)
    for i in range(num):
        distances.append([])
        for j in range(num):
            if i == j:
                distances[-1].append(0)
            elif i > j:
                distances[-1].append(distances[j][i])
            else:
                distances[-1].append(((pointX[i] - pointX[j]) ** 2 + (pointY[i] - pointY[j]) ** 2) ** 0.5)
    minimum = -1
    bestPoint = -1
    for i in range(num):
        sumDistance = sum(distances[i])
        if minimum < 0 or sumDistance < minimum:
            minimum = sum(distances[i])
            bestPoint = i
    return pointX[bestPoint], pointY[bestPoint]


parser = argparse.ArgumentParser()
parser.add_argument('--method', type=str, required=False)
parser.add_argument('--target', type=str, required=False)
parser.add_argument('--manual', type=str, required=False)
parser.add_argument('--dx', type=int, required=False)
parser.add_argument('--dy', type=int, required=False)
parser.add_argument('--std', type=int, required=False)
parser.add_argument('--r', type=float, required=False)
parsedArgs = parser.parse_args()

method = parsedArgs.method if parsedArgs.method else 'WTransE2_test'
target = parsedArgs.target.lower() if parsedArgs.target else 'venue'
manual = parsedArgs.manual
std = parsedArgs.std if parsedArgs.std else 200
centerX = 100 + 2.5 * std + (parsedArgs.dx if parsedArgs.dx else 0)
centerY = 2.5 * std + (parsedArgs.dy if parsedArgs.dy else 0)
radius = parsedArgs.r if parsedArgs.r else getDefaultDotRadius(target)

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
        coordinate = complex(float(splited[0]), float(splited[1]))
        label = splited[2]
        color = toHexColor((float(splited[3]), float(splited[4]), float(splited[5])))
        nodes.append([coordinate, label, color])
        colors[label] = color
normalize(nodes, centerX, centerY, std)
nodeNum = len(nodes)

pointX = dict()
pointY = dict()
for node in nodes:
    label = node[1]
    if not label in pointX:
        pointX[label] = []
        pointY[label] = []
    pointX[label].append(node[0].real)
    pointY[label].append(node[0].imag)

labels = []
for label in pointX.keys():
    coreX, coreY = computeCore(pointX[label], pointY[label])
    labels.append([complex(coreX, coreY), label, colors[label]])
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
canvas = Canvas(window, height=centerY + 2.25 * std + 50, width=centerX + 2.25 * std + 50, bg='white')

for node in nodes:
    createPoint(canvas, node, radius)

for label in labels:
    createLabel(canvas, label, radius, noColor=False if target in {'venue'} else True)

if target in {'venue', 'paper'}:
    venueLegend(canvas, split=True if target == 'paper' else False)

canvas.pack()
window.mainloop()
