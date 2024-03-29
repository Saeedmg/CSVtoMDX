import pandas as pd
import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.stem import PorterStemmer
import re
from hazm import *


class CSVtoMDX:
	def __init__(self, file, duplicate=True, alternates=True):
		self.file = file
		self.duplicate = duplicate
		df = pd.read_csv(self.file, sep="\t", encoding="utf-8")
		print(f"{len(df)} entries") 
		if self.duplicate:
			df.drop_duplicates(inplace=True)
			print(f"{len(df)} entries after duplicates removal:")
			self.data = df
		else:
			self.data = df
		self.alternates = alternates	

	def to_mdx(self):
		mdx = []
		for index, row in self.data.iterrows():
			# you need to add headers to your tsv file
			entry = row["ent"]
			definition = row["def"]
			# if you are converting a tsv file taken from Babylon Dictionary file .bgl, hyperlink correction
			definition = re.sub(r"bword:|BWORD:", "entry:", definition)
			mdx.append(str(entry).strip())
			# you can add your favorite font color >> replace navy!
			mdx.append("\n"+"<p style='color:navy; text-align:right; direction:rtl;'>{0}</p><br>{1}<hr>".format(entry, definition).strip())
			mdx.append("\n</>\n")
		if self.alternates: 	
			entries = mdx[0::3]
			definitions = mdx[1::3]
			print("Entries:",len(entries))
			# empty words you can add more!
			empty_words = ["هایی",r"u200c", " ","\n","","های","ی","ای",".","و","را","به","زیرا","،","از","است","باشد","بود","؛","چون","که","او","شما","تو","من","آن","آنها","این", "همه","در","بر","ها", "اند", "شده"] # You can add more
			lemmatizer =  Lemmatizer()
			ps = Stemmer()
			alters = []
			for i , j in zip(entries, definitions):
				# alternate separators
				defn = re.split(r"\s+|[0-9]+|\||\'|\"|\.|\?|-|\!|#|،|؛|:|\/|\u200c|\,|\;|\||\>|\<|«|»|\)|\(|\[|\]", i)
				for w in defn:
					if w and i and i!= "" and i is not None and w!= "" and w is not None and w not in empty_words and len(w) > 2:
						alters.append(str(w)) # use it only if you need rough verbose alternates
						alters.append("\n@@@LINK="+str(i))
						alters.append("\n</>")

						lema = str(lemmatizer.lemmatize(w))
						if "#" in lema:
							lema2 = re.split(r"#", lema)
							for ltin in lema2:
								alters.append("\n"+str(ltin))
								alters.append("\n@@@LINK="+str(i))
								alters.append("\n</>")
						else:
							if lema != "" or lema != " ":
								alters.append("\n"+str(lema))
								alters.append("\n@@@LINK="+str(i))
								alters.append("\n</>")

						stema = str(str(ps.stem(w)))
						if "#" in stema:
							stema2 = re.split(r"#", stema)
							for stin in stema2:
								alters.append("\n"+str(stin))
								alters.append("\n@@@LINK="+str(i))
								alters.append("\n</>")
						else:
							if stema !="" or stema!=" ":
								alters.append("\n"+str(ps.stem(w)))
								alters.append("\n@@@LINK="+str(i))
								alters.append("\n</>\n")		
			allents = mdx + alters
			with open('finalWithAlter.txt', 'w', encoding="UTF") as f:
				for line in allents:
					if not line.isspace():
						f.write(line)
		else:
			with open("finalNoAlternates.txt", 'w', encoding="UTF") as f:
				for line in mdx:
					if not line.isspace():
						f.write(line)				
# test file in the directory						
if __name__ == "__main__":
	a = CSVtoMDX("test2.tsv")
	a.to_mdx()

	
  					



		

      
