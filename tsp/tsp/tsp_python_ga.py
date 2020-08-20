#License
#OSI Approved :: Python Software Foundation License
#
#https://github.com/SaitoTsutomu/tsp
#
import tsp

#t = tsp.tsp([(0,0), (0,1), (0,2), (1,0), (1,1), (1,2), (2,0), (2,1), (2,2), (3,0)])

mat = [[  0,   1, 1  , 1.5, 1.6, 1.7, 1.8, 1.7, 1.6, 1.1],
       [  1,   0, 1.5,   1, 1.7, 1.8, 1.7, 1.8, 1.5, 1.2],
       [  1, 1.5,   0,   1, 1.6, 1.5, 1.6, 1.6, 1.4, 1.3],
       [1.5,   1,   1,   0, 1.4, 1.5, 1.5, 1.5, 1.3, 1.4],
       [1.4, 1.3, 1.1,   1,   0, 1.1, 1.4, 1.3, 1.2, 1.5],
       [1.5, 1.4, 1.3, 1.2,   1,   0, 1.3, 1.4, 1.1, 1.6],
       [1.7, 1.6, 1.5, 1.1,   1,   1,   0, 1.2, 1.2, 1.7],
       [1.8, 1.7, 1.6, 1.5, 1.1, 1.1,   1,   0, 1.1, 1.5],
       [1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.1,   1,   0, 1.1],
       [1.7, 1.6, 1.5, 1.4, 1.3, 1.2, 1.1, 1.3, 1.1,   0]]# Distance Matrix
r = range(len(mat))
# Dictionary of distance
dist = {(i, j): mat[i][j] for i in r for j in r}
#print(t) # distance, node index list
print( dist )
print(tsp.tsp(r, dist))
print( r )

