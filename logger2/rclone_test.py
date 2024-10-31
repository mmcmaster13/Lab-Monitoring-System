import subprocess

def update_creds():
    
    try:
        subprocess.run(["rclone config","e"],shell=False)
        
    except:
        print("failed to update rclone config")