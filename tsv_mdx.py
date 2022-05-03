import pandas as pd
import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.stem import PorterStemmer
import re


class CSVtoMDX:
	def __init__(self, file, duplicate=True, alternates=True):
		self.file = file
		self.duplicate = duplicate
		df = pd.read_csv(self.file, sep="\t", names=["ent", "def"], encoding="utf-8")
		print(f"{len(df)} entries") 
		if self.duplicate:
			df.drop_duplicates(inplace=True)
			print(f"{len(df)} entries were removed:")
			self.data = df
		else:
			self.data = df
		self.alternates = alternates	

	def to_mdx(self):
		mdx = []
		for index, row in self.data.iterrows():
			entry = row["ent"]
			definition = row["def"]
			definition = re.sub(r"bword:|BWORD:", "entry:", definition)
			mdx.append(str(entry).strip())
			mdx.append("\n"+str(definition).strip())
			mdx.append("\n</>\n")
		if self.alternates: 	
			entries = mdx[0::3]
			definitions = mdx[1::3]
			print("Entries:",len(entries))
			empty_words = ["and", "of", "for", "to", "on", "in", "up", "or","that", "this", "it", "I","off"]
			lemmatizer =  WordNetLemmatizer()
			ps = PorterStemmer()
			alters = []
			for i , j in zip(entries, definitions):
				defn = re.split(r"\s+|[0-9]+|\||\'|\"|\.|\?|-|\!|#|،|؛|:|\/|\u200c|\,|\;|\||\>|\<", i)
				for w in defn:
					if w and w not in empty_words:
						alters.append("\n"+str(w))
						alters.append("\n@@@LINK="+str(lemmatizer.lemmatize(w)))
						alters.append("\n</>")
						alters.append("\n"+str(w))
						alters.append("\n@@@LINK="+str(ps.stem(w)))
						alters.append("\n</>")		
			allents = mdx + alters
			with open('finalAlter+.txt', 'w', encoding="UTF") as f:
				for line in allents:				
					f.write(line)
		else:
			with open("final.txt", 'w', encoding="UTF") as f:
				for line in mdx:
					f.write(line)

a = CSVtoMDX("test2.tsv")
a.to_mdx()	


		

      