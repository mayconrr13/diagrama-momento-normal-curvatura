def createResultFile(limitStress, results):
    file = open('N' + str(results[0][0]) + '_' + limitStress + 'FCD.txt', "a")

    file.write('Normal Force: ' + str(results[0][0]) + '\n')
    file.write('Concrete stress: ' + str(limitStress) + '/100 fcd\n\n')
    file.write('θ, Mrd\n' )

    for j in range(len(results)):
        file.write('%.1f' % results[j][1] + ', ' + '%.6f' % results[j][2] + '\n')

    file.close()
