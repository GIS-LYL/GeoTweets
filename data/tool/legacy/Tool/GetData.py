from Tool.ToolClass import DataTransformer
import json

dataTransformer = DataTransformer()
myJson = 'var test = '
myJson += dataTransformer.toJson()
myJson += ';'
f = open('C:\\Users\\tianyi\\PhpstormProjects\\GeoTweets\\js\\auto_data.js','w')
f.write(str(myJson))
f.close()
print 'finished'