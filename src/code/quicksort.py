def Quicksort(list):
    if len(list)<=1:
        return list
    else:
        pivot = list[0]
        i = 0 #The i is used as a counter to carry out exchange operations
        #Iterate the list
        for j in range(len(list)-1):
            if list[j+1] > pivot:
                list[j+1],list[i+1] = list[i+1], list[j+1]
                i += 1

        list[0],list[i] = list[i],list[0] #Swap the pivot for the last minor element found
        #Split the list
        firts = Quicksort(list[:i])
        second = Quicksort(list[i+1:])
        firts.append(list[i])

    return (firts + second)
print(Quicksort(["B","A","C"]))