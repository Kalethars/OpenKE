def formattedRound(number, digit):
    if digit == 0:
        return str(round(number))
    else:
        rounded = str(round(number, digit))
        if not '.' in rounded:
            rounded = rounded + '.'
        return rounded + (digit - len(rounded.split('.')[1])) * '0'


def hsv2rgb(h, s=1, v=1):
    if 0 <= h < 60:
        r, g, b = 1, h / 60, 0
    elif 60 <= h < 120:
        r, g, b = (120 - h) / 60, 1, 0
    elif 120 <= h < 180:
        r, g, b = 0, 1, (h - 120) / 60
    elif 180 <= h < 240:
        r, g, b = 0, (240 - h) / 60, 1
    elif 240 <= h < 300:
        r, g, b = (h - 240) / 60, 0, 1
    elif 300 <= h < 360:
        r, g, b = 1, 0, (360 - h) / 60
    else:
        raise ValueError('Invalid hue!')
    return formattedRound(r, 6), formattedRound(g, 6), formattedRound(b, 6)


category = 'DATA'
f = open('./data/venue_%s_color.data' % category, 'r')
s = f.read().split('\n')
f.close()

venues = []
for line in s:
    splited = line.split()
    if len(splited) >= 1:
        venues.append(splited[0])
n = len(venues)

f = open('./data/colorarray.txt', 'r')
s = f.read().split('\n')
f.close()

hues = list(map(lambda x: float(x), s[n - 3].split()))
f = open('./data/venue_%s_color.data' % category, 'w')
for i in range(len(venues)):
    venue = venues[i]
    hue = hues[i * 2]
    r, g, b = hsv2rgb(hue)
    f.write('%s\t%s\t%s\t%s\n' % (venue, r, g, b))
f.close()
