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
DEMO = "Demo"
PAPER_TYPE = [PAPER, POSTER, DEMO]


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
#
# A paper contains informations add in .csv

class Paper:

    def __init__(self, conf, el):
        self.infos = el
        self.infos[CONF] = conf

        self.link = [el[LINK]]

    def addLink(self, link) :
        self.link.append(link)

    def __str__(self) : 
        return str(self.link)


# Read .csv 
def reading(path) :
    f = open(path, 'r')

    # Skip header
    f.readline()

    line = f.readline()
    while line :
        parse = line.split(SEPARATOR)

        if parse[CONF]:
            conf = parse[CONF]
            for i in PAPER_TYPE :
                conferences.append((conf , i))

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

def oneBars(i, sizes, pond, colors, legendes, names, title, save):
    bars(i, [sizes], pond, [colors], [legendes], names, title, save)

def bars(i, sizes, pond, colors, legendes, names, title, save): 

    fig = figure(i,figsize=(8,8))
    ax = fig.add_subplot(111, autoscale_on=False, xlim=(-0.65,len(names)), ylim=(0,4))

    N = len(sizes[0][0])

    # the x locations for the groups
    ind = np.arange(N)

    width = 0.35
    padding = ((len(sizes)-1)*width/2)

    m=0
    for (side, col, legende) in zip(sizes, colors, legendes) :
        acc = map(lambda x: 0, sizes[0][0])
        for (s, c, l) in zip(side, col, legende) :
            # Ajdust size with pond
            tmp = map(lambda (x,y) : x*y, zip(s,pond))

            plt.bar(ind+ m*width - padding , tmp , width, color=c, bottom=acc, label=l)
            acc = map( lambda (x,y) : x+y, zip(acc, tmp))
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

def writer(sizes, legendes, pond, names, f_name):
    f = open(f_name, 'w')
    f.write("Conferences, Total")
    map(lambda x: f.write(", {}".format(x)), legendes)
    f.write("\n")

    i = 0
    for (c,p) in zip(names, pond) :
        f.write("{}, {}, ".format(c,(1/p)*100))
        for s in sizes :
            f.write("{}, ".format(s[i]))

        i+=1
        f.write("\n")


    f.write("\n")
    f.close()
    




#  ____  _        _   
# / ___|| |_ __ _| |_ 
# \___ \| __/ _` | __|
#  ___) | || (_| | |_ 
# |____/ \__\__,_|\__|
                    

def counting(fct, li) :
    cnt = count(fct, li)
    tmp = filter(lambda x : not fct(x), li)
    
    return tmp,cnt


if( len(sys.argv[1]) < 3 ) :
    print 'Need CSV file path and STAT directory in argument'
    sys.exit(0)

CSV_FILE = sys.argv[1]
STAT_DIR = sys.argv[2]

reading(CSV_FILE)


# Remove Hardware paper
# papers = filter( lambda x : not HARD in x.infos[PINFO], papers)

# Sort paper by conference and paper type
base = map(lambda (x, t): (filter(lambda y: x in y.infos[CONF] and
                   t in y.infos[TYPE], papers), x), conferences)

# Add Global for each paper type
for i in reversed(PAPER_TYPE) :
    base.insert(0,(filter(lambda x : i in x.infos[TYPE], papers), "Global"))

# Remove empty
base = filter( lambda (x, l) : len(x) != 0, base)


i=0

nPaper      = []

nReferenced = []
nNoSoftware = []
nNoReply    = []
nReply      = []

nGiveRef    = []
nWork       = []
nPartial    = []
nPrivate    = []

names       = []
graphNames  = []

log = open("stat/log", 'w')

for (ps, n) in base :
    nPaper.append(len(ps))

    # First graph
    tmp, cnt = counting(lambda p: COMPLET in p.infos[PINFO], ps)
    nReferenced.append(cnt)
    tmp, cnt = counting(lambda p: SELF in p.infos[PINFO] or 
                             HARD in p.infos[PINFO], tmp)
    nNoSoftware.append(cnt)
    tmp, cnt = counting(lambda p: RESPONSE in p.infos[MAIL], tmp)
    nReply     .append(cnt)
    tmp, cnt = counting(lambda p: SEND in p.infos[MAIL] or
                                     WAIT in p.infos[MAIL], tmp)
    nNoReply   .append(cnt)
    
    log.write("Paper not classify in the first graph\n")
    for test in tmp :
        log.write("{}\n".format(test.infos[TITLE]))

    # Second graph
    tmp = filter(lambda p: RESPONSE in p.infos[MAIL], ps)
                            
    tmp, cnt = counting(lambda p: COMPLET in p.infos[FINFO] and
                                RESPONSE in p.infos[MAIL], tmp)
    nGiveRef.append(cnt)
    tmp, cnt = counting(lambda p: WORK in p.infos[FINFO], tmp)
    nWork.append(cnt)
    tmp, cnt = counting(lambda p: WORK not in p.infos[FINFO] and 
                            (
                                    PUBLIC not in p.infos[SCRIPT] and
                                    NONEED not in p.infos[SCRIPT] and
                                    PUBLIC in p.infos[CODE]  
                                        or
                                    PUBLIC not in p.infos[CODE] and
                                    NONEED not in p.infos[CODE] and
                                    PUBLIC in p.infos[SCRIPT] 
                            ) , tmp ) 

    nPartial.append(cnt)

    tmp, cnt = counting(lambda p: WORK not in p.infos[FINFO] and 
                                ( ( PRIVATE in p.infos[CODE] or
                                     UNAVAI in p.infos[CODE] or
                                     NONEED in p.infos[CODE] ) and (
                                     PRIVATE in p.infos[SCRIPT] or
                                     UNAVAI in p.infos[SCRIPT] ) ) , tmp)
    nPrivate.append(cnt)


    log.write("\n\nPaper not classify in the second graph\n")
    for test in tmp :
        log.write("{}\n".format(test.infos[TITLE]))


    names.append("{} - {}".format(n, ps[0].infos[TYPE]))
    graphNames.append("{} \n {}".format(n, ps[0].infos[TYPE]))


# Plot first
gSizes  = [nReferenced, nNoSoftware, nNoReply, nReply]
gNames  = ['Software referenced in paper', 'No software required', 'Authors no reply', 'Authors reply']
gPond   = map(lambda x: 100.0/x, nPaper)
gColors = ['gold', 'lightskyblue', 'lightcoral', 'yellowgreen']

oneBars(i, gSizes, gPond, gColors, gNames, graphNames, "Result of Analysis.csv", 
                "{}/global-analysis.png".format(STAT_DIR))
writer(gSizes, gNames, gPond, names, "{}/global-result.csv".format(STAT_DIR))
i+=1

# Plot second
gSizes  = [nGiveRef, nWork, nPartial, nPrivate]
gNames  = ['Give software reference', 'Work to make public release', 'Some reference', 'No reference given']
gPond   = map(lambda x: 100.0/x, nReply)
gColors = ['yellowgreen', 'lightskyblue', 'sandybrown', 'lightcoral']

oneBars(i, gSizes, gPond, gColors, gNames, graphNames, "Result of Analysis.csv", 
                "{}/mail-analysis.png".format(STAT_DIR))
writer(gSizes, gNames, gPond, names, "{}/mail-result.csv".format(STAT_DIR))
i+=1

# Plot third
gSizes  = [map(lambda (ref, noSoft, give, response): ref+noSoft+give, 
            zip(nReferenced, nNoSoftware, nGiveRef, nReply))]
gNames  = ['Reproductible paper at the end']
gPond   = map(lambda x: 100.0/x, nPaper)
gColors = ['yellowgreen']

oneBars(i, gSizes, gPond, gColors, gNames, graphNames, "Result of Analysis.csv", 
                "{}/final-analysis.png".format(STAT_DIR))
writer(gSizes, gNames, gPond, names, "{}/final-result.csv".format(STAT_DIR))

log.close()
