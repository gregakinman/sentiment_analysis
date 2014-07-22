"""
Greg Kinman - B48856
Freescale Semiconductor, Inc.

run_core_nlp.py

Runs CoreNLP, regardless of the computing platform (Windows or Unix-based).
"""

import os, subprocess

def main():

    """
    Uses Python as a cross-platform interface to access the command line to run CoreNLP. So, basically, we're using Python to run the native command-line language to then run Java...languages on languages.
    """

    # Assembles the needed .jar files.
    jar_files = [
                    "stanford-corenlp-3.4.jar", "stanford-corenlp-3.4-models.jar", "xom.jar", "joda-time.jar",
                    "jollyday.jar", "ejml-0.23.jar"
    ]

    distro_directory = "stanford-corenlp-full-2014-06-16"

    # Uses the platform-specific .jar file separator.
    if os.name == "nt":
        separator = ";"
    else:
        separator = ":"

    # Builds the .jar file paths.
    jar_file_paths = []
    for file in jar_files:
        jar_file_paths.append(os.path.join(distro_directory, file) + separator)

    jars = ""
    for path in jar_file_paths:
        jars += path

    command = [
                "java", "-cp", jars, "-Xmx1g", "edu.stanford.nlp.pipeline.StanfordCoreNLP",
                "edu.stanford.nlp.pipeline.StanfordCoreNLP", "-annotators", "tokenize,ssplit,pos,parse,sentiment",
                "-filelist", "filenames.txt", "-outputDirectory", "./snippet_files"
    ]

    subprocess.call(command)

if __name__ == "__main__":
    main()
