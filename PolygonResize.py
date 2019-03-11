import numpy as np

def FindIntersection(p1, p2, p3, p4, lines_intersect, segments_intersect, intersection, close_p1, close_p2):
    dx12 = float(p2[0] - p1[0])
    dy12 = float(p2[1] - p1[1])
    dx34 = float(p4[0] - p3[0])
    dy34 = float(p4[1] - p3[1])

    denominator = float(dy12 * dx34 - dx12 * dy34)

    t1 = float(((p1[0] - p3[0]) * dy34 + (p3[1] - p1[1]) * dx34) / denominator)

    if (np.isinf(float(t1))):
        lines_intersect = False
        segments_intersect = False
        intersection = np.array([np.nan, np.nan])
        close_p1 = np.array([np.nan, np.nan])
        close_p2 = np.array([np.nan, np.nan])

        return lines_intersect, segments_intersect, intersection, close_p1, close_p2
    
    lines_intersect = True

    t2 = float(((p3[0] - p1[0]) * dy12 + (p1[1] - p3[1]) * dx12) / -denominator)

    intersection = np.array([int(p1[0] + dx12 * t1), int(p1[1] + dy12 * t1)])

    segments_intersect = ((t1 >= 0) and (t1 <= 1) and (t2 >= 0) and (t2 <= 1))

    if (t1 < 0):
        t1 = 0
    elif (t1 > 1):
        t1 = 1
    
    if (t2 < 0):
        t2 = 0
    elif (t2 > 1):
        t2 = 1
    
    close_p1 = np.array([p1[0] + dx12 * t1, p1[1] + dy12 * t1])
    close_p2 = np.array([p3[0] + dx34 * t2, p3[1] + dy34 * t2])

    return lines_intersect, segments_intersect, intersection, close_p1, close_p2


def GetEnlargedPolygon(old_points, offset):
    new_points = []
    num_points = len(old_points)
    for j in range(num_points):
        # Find the new location for point j.
        # Find the points before and after j.
        i = j - 1
        if (i < 0):
            i += num_points
        k = int((j + 1) % num_points)

        # Move the points by the offset.
        v1 = np.array([old_points[j][0] - old_points[i][0], old_points[j][1] - old_points[i][1]])
        v1 = v1 / np.sqrt(np.sum(np.square(v1)))
        v1 *= offset
        n1 = np.array([-v1[1], v1[0]])

        pij1 = np.array([float(old_points[i][0] + n1[0]), float(old_points[i][1] + n1[1])])
        pij2 = np.array([float(old_points[j][0] + n1[0]), float(old_points[j][1] + n1[1])])

        v2 = np.array([old_points[k][0] - old_points[j][0] , old_points[k][1] - old_points[j][1]])
        v2 = v2 / np.sqrt(np.sum(np.square(v2)))
        v2 *= offset
        n2 = np.array([-v2[1], v2[0]])

        pjk1 = np.array([float(old_points[j][0] + n2[0]), float(old_points[j][1] + n2[1])])
        pjk2 = np.array([float(old_points[k][0] + n2[0]), float(old_points[k][1] + n2[1])])

        lines_intersect = []
        segments_intersect = []
        poi = [] 
        close_p1 = []
        close_p2 = []
        _, _, poi, _, _ = FindIntersection(pij1, pij2, pjk1, pjk2, lines_intersect, segments_intersect, poi, close_p1, close_p2)
        
        new_points.append([poi[0], poi[1]])
    
    return np.array(new_points)

# test
old_points = np.array([[244, 152], [420, 191], [424, 328], [157, 358]])

print("Input:")
print(old_points)

new_points = GetEnlargedPolygon(old_points, -70)
print("Output:")
print(new_points)


# Polygon visualization
import cv2
sizeImg = (960, 960)
blackRGB = np.zeros((sizeImg[0], sizeImg[1], 3), np.uint8)
cv2.polylines(blackRGB, [old_points], True, (0,255,255), 2)

cv2.polylines(blackRGB, [new_points], True, (0,0,255), 2)

cv2.imwrite("polygon.png", blackRGB)