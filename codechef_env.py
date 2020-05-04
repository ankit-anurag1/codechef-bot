from bs4 import BeautifulSoup as bs
import requests
import sys
import os
import shutil
import subprocess

if len(sys.argv) != 2:
  print("Unexpected number of command line arguments.")
  sys.exit()
else:
  url = sys.argv[1]
try:
  res = requests.get(url)
except:
  sys.exit("Could not access", url, end=".\n")

res = bs(requests.get(url).text, features="html.parser")
try:
  res = res.find(class_="dataTable").find("tbody")
except:
  sys.exit("Could not find class \"dataTable\" and/or \"tbody\".")

  
problems = res.find_all(class_="problemname")
if(len(problems) == 0):
  sys.exit("Could not find class \"problemname\".")



try:   
  problem_code = [
    problem.find(name="a")["href"][problem.find(name="a")["href"].rindex('/')+1:].lower()+".cpp"
    for problem in problems
  ]
except:
  sys.exit("Could not access problem codes.")

target_dir = r"/Users/ankitanurag/Desktop/competitive"
folder_name = 'codechef/'+url[url.rindex('/')+1:].lower()

os.chdir(target_dir)

if not os.path.exists(folder_name):
  subprocess.call(['mkdir', folder_name])
else:
  sys.exit(f"\"{folder_name}\" already exists.")

if os.path.exists(folder_name):
  os.chdir(target_dir+'/'+folder_name)
else:
  sys.exit(f"\"{target_dir}/{folder_name}\" not found.")

try:
  template = target_dir+r"/template_cpp.cpp"
  for problem in problem_code:
    subprocess.call(['cp', template, problem])
except:
  sys.exit("Could not create code files.")

print(f"Successfully created {len(problem_code)} files.")

try:
  subprocess.call(['code', './.'])
except:
  sys.exit("Could not open VS Code.")
