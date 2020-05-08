import matplotlib.pyplot as plt
import parseSVGasXML

# & "C:/Program Files (x86)/Microsoft Visual Studio/Shared/Python37_64/python.exe" -mpip install matplotlib

numbers = parseSVGasXML.numbersInPath("m -3787.5625,2736.5536 c -11.2338,-5.1267 -12.2142,-6.5549 -4.6154,-6.7237 5.3063,-0.1189 12.7945,-4.6931 16.6404,-10.1668 22.9073,-32.603 43.7337,-39.4274 74.6859,-24.4729 12.0567,5.8251 24.9031,8.3654 35.093,6.9395 l 16.0741,-2.2493 -12.636,10.1131 c -15.8078,12.652 -29.9422,12.8398 -45.4969,0.6043 -6.6486,-5.2298 -14.9085,-9.5088 -18.3552,-9.5088 -14.8323,0 -30.8181,11.839 -34.3405,25.4323 -4.4423,17.1435 -8.3174,18.5802 -27.0494,10.0323 z")
xsys =  parseSVGasXML.makeXsYs(numbers)
xsys[0] =parseSVGasXML.turnMovementsIntoPositions(xsys[0])
xsys[1] = parseSVGasXML.turnMovementsIntoPositions(xsys[1])

plt.plot(xsys[0],xsys[1])
plt.ylabel('some numbers')
plt.show()
