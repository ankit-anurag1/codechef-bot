from bs4 import BeautifulSoup as bs
import requests
import sys
import os
import shutil
import subprocess

# check if link has been provided
if len(sys.argv) != 2:
  print("Unexpected number of command line arguments.")
  sys.exit()
else:
  url = sys.argv[1]

# access the webpage
try:
  res = requests.get(url)
except:
  sys.exit("Could not access", url, end=".\n")

# using beautifulsoup to parse the html
res = bs(requests.get(url).text, features="html.parser")

# extracting the table containing problems
try:
  res = res.find(class_="dataTable").find("tbody")
except:
  sys.exit("Could not find class \"dataTable\" and/or \"tbody\".")

# extracting individual problems
problems = res.find_all(class_="problemname")
if(len(problems) == 0):
  sys.exit("Could not find class \"problemname\".")

# extracting problem code from problem-url
try:   
  problem_code = [
    problem.find(name="a")["href"][problem.find(name="a")["href"].rindex('/')+1:].lower()+".cpp"
    for problem in problems
  ]
except:
  sys.exit("Could not access problem codes.")


# my directory structure :
# home -> Users -> ankitanurag -> Desktop -> competitive ->
# codechef -> event_folder

target_dir = r"/Users/ankitanurag/Desktop/competitive"

# extract event code from page url - ignores query params
folder_name = 'codechef/'+url[url.rindex('/')+1:url.index('?')].lower()


os.chdir(target_dir)

# create directory if it does not exist
if not os.path.exists(folder_name):
  subprocess.call(['mkdir', folder_name])
else:
  print(f"\"{folder_name}\" already exists.")
  ow = input("Overwrite contents of folder? (y/n) ")
  if ow != 'y' or ow != 'Y':
    sys.exit("Aborting...")

# redundant safety check for switching to created event folder
if os.path.exists(folder_name):
  os.chdir(target_dir+'/'+folder_name)
else:
  sys.exit(f"\"{target_dir}/{folder_name}\" not found.")

# creating cpp files for individual problems
# template directory structure:
# home -> Users -> ankitanurag -> Desktop -> competitive -> template_cpp.cpp
try:
  template = target_dir+r"/template_cpp.cpp"
  for problem in problem_code:
    subprocess.call(['cp', template, problem])
except:
  sys.exit("Could not create code files.")

print(f"Successfully created {len(problem_code)} files.")

# for VSCode, if added to path
try:
  subprocess.call(['code', './.'])
except:
  sys.exit("Could not open VS Code.")
