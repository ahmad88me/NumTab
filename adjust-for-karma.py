import random
numtab = open('gold/numtab.txt', 'a+')

list_of_lists = []
list = []
for line in numtab:
        if line.startswith('http'):
                list_of_lists.append(list)
                list = [line]
        else:
                list.append(line)

counter = 0
random.shuffle(list_of_lists)
for x in range(0, len(list_of_lists)):
        print x
        file = open('gold/files/file' + str(counter) + '.txt', 'a+')
        file.write('\n'.join(list_of_lists[x]) + '\n\n')
        if (x%10) is 0:
                counter+=1
        file.close()