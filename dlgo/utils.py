from dlgo import gotypes

COLS = 'ABCDEFGHJKLMNOPQRST'

def point_from_coords(coords):
    col = COLS.index(coords[0]) + 1
    row = int(coords[1:])
    return gotypes.Point(row=row, col=col)