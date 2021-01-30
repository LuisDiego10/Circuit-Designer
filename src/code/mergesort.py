#Function performs the comparisons and joins the elements to show the result
def merge(left,right):
    result=[]
    i,j=0,0
    while i<len(left) and j<len(right):
        if left[i]<=right[j]:
            result.append(left[i])
            i+=1
        else:
            result.append(right[j])
            j+=1
    result+=left[i:]
    result+=right[j:]
    return result

#Function that divides the list and points to the middle
def mergesort(list):
    if len(list)<=1:
        return list
    mid=int(len(list)/2)
    left=mergesort(list[:mid])
    right=mergesort(list[mid:])
    return merge(left,right)

print(mergesort(["2","1","3"]))
