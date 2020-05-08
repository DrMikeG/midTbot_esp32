

def pointInLine(A,B, valueT) :
    ax = A[0]
    ay = A[1]
    bx = B[0]
    by = B[1]
    cx = ax - ((ax- bx) * valueT)
    cy = ay - ((ay - by) * valueT)
    return [cx,cy]

def interpCubic(p0,p1,p2,p3,T):
    A = pointInLine(p0, p1, T)
    B = pointInLine(p1, p2, T)
    C = pointInLine(p2, p3, T)
    D = pointInLine(A, B, T) # // The new D
    E = pointInLine(B, C, T) # // and E
    F = pointInLine(D, E, T) # // The juicy one
    return F

def getTValues():
    Ts = []
    for i in range(11):
        Ts.append(i/10.0)
    return Ts

def getCubicTupleIndices(xsys):
    ## 0:4: returns 0,1,2,3
    #vs = bez.tenStepsCubic(xsys[0][0:4:],xsys[1][0:4:])
    # 3:7 return 3,4,5,6
    #vs2 = bez.tenStepsCubic(xsys[0][3:7:],xsys[1][3:7:])
    #Generalise for len

    assert len(xsys) == 2, "output area should be the same length as input"
    assert len(xsys[0]) == len(xsys[1]) , "output area should be the same length as input"

    tupleArrayOfIndices = []
    i = 0
    while i+3 <= len(xsys[0])-1:
        arrayOfIndicesFromI = [i,i+1,i+2,i+3]
        tupleArrayOfIndices.append(arrayOfIndicesFromI)
        i += 3
    # = [[0,1,2,3],[3,4,5,6]]
    
    return tupleArrayOfIndices

def tenStepsCubic(Xs,Ys):
    xPointsOnCurve = []
    yPointsOnCurve = []
    for T in getTValues():
        P = interpCubic(
        [Xs[0],Ys[0]],
        [Xs[1],Ys[1]],
        [Xs[2],Ys[2]],
        [Xs[3],Ys[3]],T)
        xPointsOnCurve.append(P[0])
        yPointsOnCurve.append(P[1])
    return [xPointsOnCurve,yPointsOnCurve]

def tenStepsOnPolyCubic(xsys):
    indices = getCubicTupleIndices(xsys)
    vsXs = []
    vsYs = []
    
    for ind in indices:
        xs = [ xsys[0][ind[0]], xsys[0][ind[1]], xsys[0][ind[2]], xsys[0][ind[3]] ]
        ys = [ xsys[1][ind[0]], xsys[1][ind[1]], xsys[1][ind[2]], xsys[1][ind[3]] ]
        XsYspoints = tenStepsCubic(xs,ys)
        vsXs += XsYspoints[0]
        vsYs += XsYspoints[1]
    return [vsXs,vsYs]