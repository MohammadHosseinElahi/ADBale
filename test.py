i = [{"ali":11},"hasan",{"asghar":[1,2,3]}]
# print(i.index({"ali"}))
b = {"496133841": ['LOGGED_IN', 'rp1', {'ad': ['slkdjf']}]}
def find_index(index,List):
    for i in List:
        if index in i:
            return List.index(i) 
    return False 

print(find_index("ad",b["496133841"]))



