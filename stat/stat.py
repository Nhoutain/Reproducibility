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

def bars(i, sizes, colors, legendes, names, title, save): 

    fig = figure(i,figsize=(8,8))
    ax = fig.add_subplot(111, autoscale_on=False, xlim=(-0.65,7), ylim=(0,4))

    N = len(sizes[0][0])

    # the x locations for the groups
    ind = np.arange(N)

    width = 0.35
    padding = ((len(sizes)-1)*width/2)

    m=0
    for (side, col, legende) in zip(sizes, colors, legendes) :
        acc = map(lambda x: 0, sizes[0][0])
        for (s,c, l) in zip(side, col, legende) :
            plt.bar(ind+ m*width - padding , s, width, color=c, bottom=acc, label=l)
            acc = map( lambda (x,y) : x+y, zip(acc, s))
        m += 1


    plt.ylabel('Pourcentage')
    plt.title(title)

    plt.xticks(ind+width/2., names, rotation='vertical' )
    plt.margins(0.3)
    # Tweak spacing to prevent clipping of tick-labels
    plt.subplots_adjust(bottom=0.25)

    plt.yticks(np.arange(0,101,10))

    plt.legend(loc=2)

    savefig(save)





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
#for (ps, n) in base :
#    nSend     = count(lambda p: SEND in p.infos[MAIL], ps)
#    nResponse = count(lambda p: RESPONSE in p.infos[MAIL], ps)
#    nComplet  = count(lambda p: COMPLET in p.infos[PINFO], ps)
#    nSelf     = count(lambda p: SELF in p.infos[PINFO], ps)
#    nHardware = count(lambda p: HARD in p.infos[PINFO], ps)
#    nMail     = len(ps)
#
#    camenbert(i,[nSend, nResponse, nComplet, nSelf, nHardware],
#                ['No reply', 'Response', 'Complet', 'Self', 'Hardware'] , 1000, "piechart_mail/piechart_mail-{}.png".format(n))
#    i+=1


nSend     = []
nResponse = []
nComplet  = []
nSelf     = []
nHardware = []
nMail     = []
names     = []

for (ps, n) in base :
    nMail = len(ps)
    nSend    .append( (100.0/nMail)*count(lambda p: SEND in p.infos[MAIL], ps) )
    nResponse.append( (100.0/nMail)*count(lambda p: RESPONSE in p.infos[MAIL], ps) )
    nComplet .append( (100.0/nMail)*count(lambda p: COMPLET in p.infos[PINFO], ps) )
    nSelf    .append( (100.0/nMail)*count(lambda p: SELF in p.infos[PINFO], ps) )
    nHardware.append( (100.0/nMail)*count(lambda p: HARD in p.infos[PINFO], ps) )
    names    .append(n)


bars(i,[[nComplet, nSelf, nHardware], [nSend, nResponse]],
            [['r', 'g', 'b'], ['y', 'r']],
            [['Complet', 'Self contains', 'Hardware'], ['Wait response', 'Response']],
            names, "Result of Analysis.csv", 'bar_mail/bar_mail-all.png')
                #['No reply', 'Response', 'Complet', 'Self', 'Hardware'] , 1000, "piechart_mail/piechart_mail-{}.png".format(n))

i+=1

#bars(1, [[20, 35, 30, 35, 27], [25, 32, 34, 20, 25], [31, 37, 2, 26, 20]], ['y', 'r', 'g'])


