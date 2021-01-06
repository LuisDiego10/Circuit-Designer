def Quicksort(list):
    print("Lista: ",list)
    if len(list) == 1 or len(list) == 0:
        return list
    else:
        pivot = list[0]
        i = 0 #El i es utilizado como contador para cuando aparezca un elemento menor al pivot
        #Recorre la lista
        for j in range(len(list)-1):
            if list[j+1] < pivot:
                list[j+1],list[i+1] = list[i+1], list[j+1]
                i += 1

        list[0],list[i] = list[i],list[0]#Intercambiar el pivot por el último elemento menor encontrado
        #Dividir la lista
        firts = Quicksort(list[:i])
        print("Firts",firts)
        second = Quicksort(list[i+1:])
        print("Second",second)
        firts.append(list[i])

    return (firts + second)
print(Quicksort([7,3,4]))