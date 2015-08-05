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
WORK = "Work"
PRIVATE = "Private"
PUBLIC = "Public"
NONEED = "No need"
WAIT = "Wait"
UNAVAI = "No available"

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
                   
def camenbert(i, sizes, labels, colors, explode, dpi, save, isLegend) :
    fig = figure(i,figsize=(8,5))
    ax = fig.add_subplot(111, autoscale_on=False, xlim=(-1,5), ylim=(-4,3))


    patches, texts = plt.pie(sizes, explode=explode, colors=colors,
            shadow=True, startangle=90)

    # Set aspect ratio to be equal so that pie is drawn as a circle.
    plt.axis('equal')

    if isLegend :
        plt.legend(patches, labels, loc='best')

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
    plt.margins(0.5)
    # Tweak spacing to prevent clipping of tick-labels
    plt.subplots_adjust(bottom=0.28)

    plt.yticks(np.arange(0,111,10))

    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.28),
                      fancybox=True, shadow=True, ncol=2)

    savefig(save)



#  ____  _        _   
# / ___|| |_ __ _| |_ 
# \___ \| __/ _` | __|
#  ___) | || (_| | |_ 
# |____/ \__\__,_|\__|
                    


if( len(sys.argv[1]) < 3 ) :
    print 'Need CSV file path and STAT directory in argument'
    sys.exit(0)

CSV_FILE = sys.argv[1]
STAT_DIR = sys.argv[2]

reading(CSV_FILE)


# Papers by conference and remove hardware
base = map(lambda x: (filter(lambda y: x in y.infos[CONF] and
                   not HARD in y.infos[PINFO] and
                   PAPER in y.infos[TYPE], papers), x), conferences)

base.insert(0,(papers, "Global"))

# Generated piechart 
i=0

nPaper      = []
nReferenced = []
nNoSoftware = []
nNoReply    = []
nReply      = []

nGiveRef    = []
nWork       = []
nPrivate    = []

names       = []


for (ps, n) in base :
    nPaper.append(len(ps))
    nPaperReply = count(lambda p: RESPONSE in p.infos[MAIL], ps) 

    # First graph
    nReferenced.append((100.0/nPaper[-1])*count(lambda p: COMPLET in p.infos[PINFO], ps) )
    nNoSoftware.append((100.0/nPaper[-1])*count(lambda p: SELF in p.infos[PINFO] or 
                             HARD in p.infos[PINFO], ps) )
    nReply     .append((100.0/nPaper[-1])*count(lambda p: RESPONSE in p.infos[MAIL], ps) )
    nNoReply   .append((100.0/nPaper[-1])*count(lambda p: SEND in p.infos[MAIL] or
                                     WAIT in p.infos[MAIL], ps) )


    # Second graph
    nGiveRef   .append((100.0/nPaperReply)*count(lambda p: COMPLET in p.infos[FINFO] and
                                                    RESPONSE in p.infos[MAIL], ps) )
    nWork      .append((100.0/nPaperReply)*count(lambda p: WORK in p.infos[FINFO], ps) )
    nPrivate   .append((100.0/nPaperReply)*count(lambda p: WORK not in p.infos[FINFO] and 
                                (   PRIVATE in p.infos[CODE] or
                                     UNAVAI in p.infos[CODE] or
                                     PRIVATE in p.infos[SCRIPT] or
                                     UNAVAI in p.infos[SCRIPT] ) , ps) )

    names.append(n)


print("{} = {} {} {} {}".format(nPaper, nReferenced, nNoSoftware, nReply, nNoReply))

bars(i,[[nReferenced, nNoSoftware, nNoReply, nReply]],
            [['gold', 'lightskyblue', 'lightcoral', 'yellowgreen']],
            [['Software referenced in paper', 'No software required', 'Authors no reply', 'Authors reply']],
            names, "Result of Analysis.csv", "{}/bar_mail/bar_mail-all.png".format(STAT_DIR))

i+=1

bars(i,[[nGiveRef, nWork, nPrivate]],
            [['yellowgreen', 'lightskyblue', 'lightcoral']],
            [['Give software reference', 'Work to make a public release', 'No software or script available']],
            names, "Result of Analysis.csv", "{}/bar_mail/bar_mail2-all.png"
                                                .format(STAT_DIR))
i+=1

bars(i,[[map(lambda (ref, noSoft, give, response): ref+noSoft+(give*response/100.), zip(nReferenced,nNoSoftware, nGiveRef, nReply))]],
            [['yellowgreen']],
            [['Reproductible paper at the end']],
            names, "Result of Analysis.csv", "{}/bar_mail/bar_mail3-all.png"
                                                .format(STAT_DIR))

