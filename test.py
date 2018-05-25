import glob, os
os.chdir("images")
faces = []
for file in glob.glob("*.jpg"):
	faces.append(file)
	print(file)
print(faces)
