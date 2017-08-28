import argparse
import os
from collections import defaultdict

import numpy as np
import pandas as pd
from nltk.tokenize import word_tokenize

parser = argparse.ArgumentParser(description='preparing vocabulary for simple questions dataset')
parser.add_argument('-i', '--input', help='input file path tab separated triples', required=True)
parser.add_argument('-fe', '--entfilter', help='file containing list of entities to filter upon [newline sep]', required=False)
parser.add_argument('-fp', '--propfilter', help='file containing list of properties to filter upon [newline sep]', required=False)
parser.add_argument('-o', '--output', help='output folder path to save all generated files in', required=True)
args = parser.parse_args()


props = None
ents = None
BASE_URI = "http://www.wikidata.org/entity/"
BASE_URI2 = "http://www.wikidata.org/prop/direct"

fout = open(os.path.join(args.output,"tmp.txt"), "w")

if args.propfilter is not None:
    props = []
    with open(args.entfilter) as f:
        for l in f:
            props.append(l.strip())
    props = dict(zip(props, range(len(props))))

if args.entfilter is not None:
    ents = []
    with open(args.entfilter) as f:
        for l in f:
            ents.append(l.strip())
    ents = dict(zip(ents, range(len(ents))))


triples_count = 0
scanned = 0
with open(args.inputs) as f:

    for l in f:
        scanned += 1
        s, p, o = [i.strip().replace(BASE_URI, "").replace(BASE_URI2, "") for i in l.split("\t")]

        if s in ents and p in props and o in ents:
            triples_count += 1
            s = ents[s]
            p = props[p]
            o = ents[o]

            fout.write("%s\t%s\t%s\n" % (s, o, p))

        if scanned % 1000 == 0:
            print("%s triples scanned .. " % scanned)



fout.close()

print("finalizing triples 2 ids file ...")
with open(os.path.join(args.output, "triple2id.txt"),"w") as fout:

    fout.write(str(triples_count) + "\n")
    with open(os.path.join(args.output, "tmp.txt"),"r") as f:
        for l in f:
            fout.write(l)

print("creating entities 2 ids file ...")
with open(os.path.join(args.output, "entity2id.txt"), "w") as fout:

    fout.write(str(len(ents)) + "\n")

    for i in zip(ents.keys(), ents.values()):
        fout.write("%s\t%s\n" % (i[0], i[1]))

print("creating relation 2 ids file ...")
with open(os.path.join(args.output, "relation2id.txt"), "w") as fout:
    fout.write(str(len(props)) + "\n")

    for i in zip(props.keys(), props.values()):
        fout.write("%s\t%s\n" % (i[0], i[1]))



































