# #!/usr/bin/python3
#
# import os
# import requests
# from termcolor import colored
# import subprocess
# import shutil
#
# # global variable
# home_dir = os.path.expanduser("~") + '/.drivers/'
# if not os.path.exists(home_dir):
#     os.system(f'mkdir {home_dir}')
#
#
# # downloading driver
# def download_driver(url, path, filename, new_file):
#     r = requests.get(url, stream=True)
#     with open(filename, "wb") as f:
#         shutil.copyfileobj(r.raw, f)
#     os.system(f"unzip {filename}")
#     os.system(f"mv {new_file} {path}")
#     os.system(f"rm {filename}")
#     print(colored("[+] Successfully downloaded the driver...", 'green'))
#
#
# # driver
# def fetching_driver(system_chrome_ver):
#     try:
#         version_li = ['88.0.4324.27', '87.0.4280.20', '86.0.4240.22', '85.0.4183.38', '84.0.4147.30', '83.0.4103.14']
#         for i in version_li:
#             if i.split(".")[0] == system_chrome_ver:
#                 driver_ver = i
#                 break
#         url = f'https://chromedriver.storage.googleapis.com/{driver_ver}/chromedriver_linux64.zip'
#         filename = url.split("/")[-1]
#         new_file = filename.split("_")[0]
#         if not os.path.exists(home_dir + new_file):
#             print(colored("[-] driver not found, Please wait downloading the driver...", 'red'))
#             download_driver(url, home_dir, filename, new_file)
#         return home_dir + new_file
#     except:
#         print(colored("[++] Somethings error", 'red'))
#
#
# # checking system browser
# def driver():
#     try:
#         ver = subprocess.check_output('chromium --version', shell=True)
#         system_chrome_ver = ver.decode('utf-8').split(" ")[1].split(".")[0]
#     except:
#         ver = subprocess.check_output('google-chrome --version', shell=True)
#         system_chrome_ver = ver.decode('utf-8').split(" ")[2].split(".")[0]
#
#     return fetching_driver(system_chrome_ver)
