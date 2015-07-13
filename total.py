

def parse(s) :
    res = s.split()
    start_h, start_m = map(int, res[2].split('h'))
    end_h, end_m = map(int, res[4].split('h'))
    minus_h, minus_m = map(int, res[6].split('h'))

    return (res[0], (end_h-start_h-minus_h)*60 + (end_m-start_m-minus_m))


total = 0
days  = 0

for line in open("horaire.txt") :
    if "/" in line :
        (date, mins) = parse(line)

        total += mins
        days  += 1
        print( "On {} you work {}h{}".format(date, mins/60, mins%60) )


print( "---" )
print( "Total : {}h{} on {} days  =>  {}h{} in average".format(total/60, total%60, days, total/60/days, (total/days)%60) )



