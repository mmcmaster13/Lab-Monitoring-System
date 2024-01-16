from discord_ex import post_alert

def do_checks(labeled_data, thresholds, crit_counts):
    
    #we can make the measurers send thresholds every time; this is kind of the only way to do it
    #if we want to leave the collector out of everything
    
    if len(crit_counts) == 0:
        
        for key in labeled_data:
            crit_counts[key] = 0
    
    for key in labeled_data:

        if key == "780 Cooling Status" or key == "780 Repump Status":
            data = -labeled_data[key]
            threshold = -thresholds[key]
        else:
            data = labeled_data[key]
            threshold = thresholds[key]
        
        crit_count = crit_counts[key]
        
        if data > threshold and crit_count < 20:
            
            crit_counts[key] = crit_count + 1
            
        elif data > threshold and crit_count == 20:
            
            crit_counts[key] = 0
            
            alert = str(key) + " has been measured above the threshold for at least 20 minutes. Actual mesaured value is: " + str(data)
            
            #post_alert(alert)
            
            print(alert)
            
        else:
            continue
        
        return crit_counts
