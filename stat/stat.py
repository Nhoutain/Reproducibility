from pylab import *
from math import *
import matplotlib.pyplot as plt

#   ____                _              _       
#  / ___|___  _ __  ___| |_ __ _ _ __ | |_ ___ 
# | |   / _ \| '_ \/ __| __/ _` | '_ \| __/ _ \
# | |__| (_) | | | \__ \ || (_| | | | | ||  __/
#  \____\___/|_| |_|___/\__\__,_|_| |_|\__\___|
                                             

SEPARATOR = ','

CONF   = 0
TITLE  = 1
DOI    = 2
TYPE   = 3
CAT    = 4
PINFO  = 5
MAIL   = 6
FINFO  = 7
CODE   = 8
SCRIPT = 9
SHARE  = 10
COM    = 11
LINK   = 12

SEND = "Send"
RESPONSE = "Response"
SELF = "Self contains"
HARD = "Hardware"
COMPLET = "Complet"

PAPER = "Paper"
POSTER = "Poster"


#   ____ _       _           _ 
#  / ___| | ___ | |__   __ _| |
# | |  _| |/ _ \| '_ \ / _` | |
# | |_| | | (_) | |_) | (_| | |
#  \____|_|\___/|_.__/ \__,_|_|
                             
papers = []
conferences = []

#  ____                       
# |  _ \ __ _ _ __   ___ _ __ 
# | |_) / _` | '_ \ / _ \ '__|
# |  __/ (_| | |_) |  __/ |   
# |_|   \__,_| .__/ \___|_|   
#            |_|              

class Paper:

    def __init__(self, conf, el):
        self.infos = el
        self.infos[CONF] = conf

        self.link = [el[LINK]]

    def addLink(self, link) :
        self.link.append(link)

    def __str__(self) : 
        return str(self.link)


def reading(path) :
    f = open(path, 'r')

    # Skip header
    f.readline()

    line = f.readline()
    while line :
        parse = line.split(SEPARATOR)

        if parse[CONF]:
            conf = parse[CONF]
            conferences.append(conf)

        if parse[TITLE]:
            paper = Paper(conf, parse)
            papers.append(paper)
        elif parse[LINK] :
            paper.addLink(parse[LINK])

        line = f.readline()

    f.close()

def count(fct, l) : 
    return sum(map(fct, l))

#  ____  _       _   
# |  _ \| | ___ | |_ 
# | |_) | |/ _ \| __|
# |  __/| | (_) | |_ 
# |_|   |_|\___/ \__|
                   
def camenbert(i, sizes, labels, dpi, save) :
    fig = figure(i,figsize=(8,5))
    ax = fig.add_subplot(111, autoscale_on=False, xlim=(-1,5), ylim=(-4,3))

    colors = ['red', 'yellowgreen', 'gold', 'lightskyblue','lightcoral']
    explode = (0.1, 0.1, 0.1, 0.1, 0.1) 
    plt.pie(sizes, explode=explode, labels=labels, colors=colors,
            autopct='%1.1f %% ', shadow=True, startangle=90)

    # Set aspect ratio to be equal so that pie is drawn as a circle.
    plt.axis('equal')

    savefig(save)

    #plt.show()


#  ____  _        _   
# / ___|| |_ __ _| |_ 
# \___ \| __/ _` | __|
#  ___) | || (_| | |_ 
# |____/ \__\__,_|\__|
                    


reading("../Analysis.csv")


# Papers by conference

base = map(lambda x: (filter(lambda y: x in y.infos[CONF], papers), x), conferences)
base.insert(0,(papers, "Global"))

# Generated piechart 
i=0
for (ps, n) in base :
    nSend = count(lambda p: SEND in p.infos[MAIL], ps)
    nResponse = count(lambda p: RESPONSE in p.infos[MAIL], ps)
    nComplet = count(lambda p: COMPLET in p.infos[PINFO], ps)
    nSelf = count(lambda p: SELF in p.infos[PINFO], ps)
    nHardware = count(lambda p: HARD in p.infos[PINFO], ps)
    nMail = len(ps)

    camenbert(i,[nSend, nResponse, nComplet, nSelf, nHardware],
                ['No reply', 'Response', 'Complet', 'Self', 'Hardware'] , 1000, "piechart_mail/piechart_mail-{}.png".format(n))
    i+=1




