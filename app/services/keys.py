from app.services.dict2 import equipment as dic2
keys3=[]
for key in dic2.keys():
    if len(key.split(" "))==2:
        keys3.append(key.split(" ")[0]+"-"+key.split(" ")[1]+" "+key.split(" ")[0]+key.split(" ")[1]+key)
    elif len(key.split(" "))==3:
        keys3.append((key.split(" ")[0]+"-"+key.split(" ")[1]+" "+key.split(" ")[0]+key.split(" ")[1]+" "+
                      key.split(" ")[1]+"-"+key.split(" ")[2]+" "+key.split(" ")[1]+key.split(" ")[2]+" "+
                      key.split(" ")[0] + "-" + key.split(" ")[2] + " " + key.split(" ")[0] + key.split(" ")[2] +" "+
                      key.replace("-","")  +
                      key))
    elif len(key.split(" "))==4:
        keys3.append((key.split(" ")[0] + "-" + key.split(" ")[1] + " " + key.split(" ")[0] + key.split(" ")[1] + " "+
                      key.split(" ")[1] + "-" + key.split(" ")[2] + " " + key.split(" ")[1] + key.split(" ")[2] +" "+
                      key.split(" ")[2] + "-" + key.split(" ")[3] + " " + key.split(" ")[2] + key.split(" ")[3] +" "+
                      key.split(" ")[0] + "-" + key.split(" ")[2] + " " + key.split(" ")[0] + key.split(" ")[2] +" "+
                      key.split(" ")[0] + "-" + key.split(" ")[3] + " " + key.split(" ")[0] + key.split(" ")[3] + " " +
                      key.replace("-", "") +
                      key))
    elif len(key.split(" "))==5:
        keys3.append((key.split(" ")[0] + "-" + key.split(" ")[1] + " " + key.split(" ")[0] + key.split(" ")[1] +" "+
                      key.split(" ")[1] + "-" + key.split(" ")[2] + " " + key.split(" ")[1] + key.split(" ")[2] +" "+
                      key.split(" ")[2] + "-" + key.split(" ")[3] + " " + key.split(" ")[2] + key.split(" ")[3] +" "+
                      key.split(" ")[0] + "-" + key.split(" ")[2] + " " + key.split(" ")[0] + key.split(" ")[2] +" "+
                      key.split(" ")[0] + "-" + key.split(" ")[3] + " " + key.split(" ")[0] + key.split(" ")[3] + " " +
                      key.replace("-", "") +
                      key))