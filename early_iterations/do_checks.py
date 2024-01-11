from discord_ex import post_alert

names = ["Main Chamber Pressure", "Yb Oven Temperature", "Rb Supply Current"]
units = ["torr", "C", "A"]

def do_checks(data_arr, crit_count, thresholds):
    
    for i in range(0,3):
        
        point = data_arr[i]
        threshold = thresholds[i]
        count = crit_count[i]
        
        if point >= threshold and count < 5:
            crit_count[i] += 1
        elif point >= threshold and count == 5:
            crit_count[i] = 0
            post_alert(names[i] + " threshold exceeded for at least five minutes. Value: " + str(point) + units[i])
        else:
            continue
    
    return crit_count
