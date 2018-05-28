#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Questo script è utilizzato creare automaticamente i file snippets corrispondenti
ai blocchi di codice della guida in modo che possano essere visualizzati
cliccando sul pulsantino di fianco al titolo
"""
from __future__ import print_function
import io,os
import shutil

TARGET_DIR = "snippets"

# Reset the output folder
if os.path.isdir(TARGET_DIR):
	for the_file in os.listdir(TARGET_DIR):
	    file_path = os.path.join(TARGET_DIR, the_file)
	    try:
	        if os.path.isfile(file_path):
	            os.unlink(file_path)
	    except Exception as e:
	        print(e)
else:
	os.makedirs(TARGET_DIR)

def save_file(current_lines, chapter_count, section_count, subsect_count):
	if len(current_lines) == 0:
		current_lines.append("Il paragrafo non conteneva codice.")
	# Save the current code
	filename=TARGET_DIR+os.sep+str(chapter_count)+"."+str(section_count)+"."+str(subsect_count)+".txt"
	with open(filename, 'w') as output_file:
		for current_line in current_lines:
			output_file.write(current_line)

with io.open('guida.tex', mode='r', encoding="utf-8") as tex_file:
	current_lines = []

	chapter_count = 0
	section_count = 0
	subsect_count = 0

	inside_code = False

	for line in tex_file.readlines():
		line = line.replace("\r","")

		if inside_code and not line.strip().startswith("\\end{lstlisting}"):
			current_lines.append(line)

		if line.startswith("\\chapter"):
			save_file(current_lines, chapter_count, section_count, subsect_count)
			current_lines = []

			chapter_count+=1
			section_count=0
			subsect_count=0
		elif line.startswith("\\section"):
			save_file(current_lines, chapter_count, section_count, subsect_count)
			current_lines = []

			section_count+=1
			subsect_count=0
		elif line.startswith("\\subsection"):
			save_file(current_lines, chapter_count, section_count, subsect_count)
			current_lines = []

			subsect_count+=1
		elif line.strip().startswith("\\begin{lstlisting}"):
			inside_code = True
			current_lines.append("########################### CODE ###########################\n")
		elif line.strip().startswith("\\end{lstlisting}"):
			inside_code = False
			current_lines.append("############################################################\n")
