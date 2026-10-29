from build123d import *
import numpy as np

def heightGetting(obj, x_meas, y_meas):
    p = (x_meas, y_meas, height)
    # Create a vertical axis at (target_x, target_y, high_z) pointing along -Z
    vertical_axis = Axis(p, (0, 0, -1))

    # Intersect the axis with the part and get the highest Z intersection vertex
    intercepts = vertical_axis.intersect(obj)
    try:
        top_vertex = intercepts.vertices().sort_by(Axis.Z)[-1]
    except AttributeError:
        return 0
        #print("Height is None")
    else:
        return top_vertex.Z
        #matrix[x_arr, y_arr, 2] = height_z
        #print(f"Height is {height_z}")

height = 300
numPoints = 100


test = import_step("./test.step")
test_bound = test.bounding_box()
print(type(test_bound))
print(test_bound.max / IN)
print(test_bound.min)
xBound = test_bound.max.X - test_bound.min.X
yBound = test_bound.max.Y - test_bound.min.Y

print(xBound)
print(yBound)


#given
#distance between each point made by sensor (determined by sensing
# frequency and motor speed)
# x and y size of bound box

xArr = np.linspace(test_bound.min.X, test_bound.max.X, num = numPoints)
yArr = np.linspace(test_bound.min.Y, test_bound.max.Y, num = numPoints)

print(xArr)
print(yArr)

thing = np.zeros((numPoints, numPoints, 3))

#change this to a mapping function
for i in range(numPoints):
    for j in range(numPoints):
        thing[i, j, 0] = xArr[i]
        thing[i, j, 1] = yArr[j]

for i in range(numPoints):
    for j in range(numPoints):
        thing[i, j, 2] = heightGetting(test, xArr[i], yArr[j])

# print(thing)
#
# # 2d array of x coords
# print(thing[:,:,0])
#
# # 2d array of y coords
# print(thing[:,:,1])
#
# # 2d array of heights
# print(thing[:,:,2])

flat_strings = [np.array2string(inner, separator=': ') for layer in thing for inner in layer]
result_arr = np.array(flat_strings).reshape(thing.shape[:2])

np.savetxt("output_numpy.csv", result_arr, delimiter=",", fmt="%s")


#goal
# split box into grid with equal squares (with the last
# square rounded if needed
# put axis for measure in the middle of each square



x = 6.35
y = 12.7
p_test = (x, y, height)


# # Create a vertical axis at (target_x, target_y, high_z) pointing along -Z
# vertical_axis = Axis(p, (0, 0, -1))
#
# # Intersect the axis with the part and get the highest Z intersection vertex
# intercepts = vertical_axis.intersect(test)
# try:
#     top_vertex = intercepts.vertices().sort_by(Axis.Z)[-1]
# except AttributeError:
#     print("Height is None")
# else:
#     height_z = top_vertex.Z
#     print(f"Height is {height_z}")





# find bottom of shape
# make plane ___ up above shape
# calcuate x and y of bounding box, then multiply to find xy bound area
# divide area by frequency to get number of samples
# divide number of samples by number of rows to get samples per row (figure out a way to decide number of rows)
# calcuate distance from plane to top of object

