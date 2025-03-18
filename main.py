import subprocess
import platform
import re
import matplotlib.pyplot as plt
import pandas as pd

def ping(host, count):
    if count < 1:
        return "Please insert at least 1 ping"

    pings_data = []

    if platform.system() == "Windows":
        command = ["ping", "-n", str(count), host]  # for Windows
    else:
        command = ["ping", "-c", str(count), host] # for UNIX

    try:
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        for line in process.stdout:
            print(line.strip())
            match_rec = re.search(r"time[= ]([\d.]+) ms", line)
            match_loss = re.search(r"Request timeout for icmp_seq", line)
            if match_rec:
                response_time = float(match_rec.group(1))
                pings_data.append({"ping_num": len(pings_data) + 1, "response_time": response_time})
            if match_loss:
                pings_data.append({"ping_num": len(pings_data) + 1, "response_time": float("nan")})

        process.wait()
        if process.returncode != 0:
            print(f"Error:{host} is not responding")

    except Exception as e:
        print(f"Error during ping execution: {e}")

    return pings_data

def plot_package_loss_pie(df):
    pack_loss = df["response_time"].isnull().sum()
    pack_rec = len(df) - pack_loss
    sizes = [pack_loss, pack_rec]
    labels = ["Packages Lost", "Packages Received"]
    plt.figure(figsize = (12, 8))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', colors = ['#1f77b4', '#ff7f0e'])
    plt.title('Package Loss Pie')
    plt.axis('equal')

def get_pings_and_plot(host, count):
    pings_df = pd.DataFrame(ping(host, count))
    pings_df["response_time"].hist(bins=20, edgecolor="black")
    plt.xlabel("Response Time")
    plt.ylabel("Frequency")
    plt.title("Response Time Plot for " + str(count) + " Pings")
    plot_package_loss_pie(pings_df)
    plt.show()

host = str(input("Enter Host: "))
get_pings_and_plot(host, int(input("Enter number of pings: ")))