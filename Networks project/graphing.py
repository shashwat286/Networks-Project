import matplotlib.pyplot

def genarategraph(filename1,filename2,title):
    graphfile1=open(f'results/{filename1}.txt')
    lines1=graphfile1.readlines()
    x1 = []
    y1 = []
    for line in lines1:
        parts=(line.strip()).split(" ")
        x1.append(int(parts[0]))
        y1.append(float(parts[1]))
        
    graphfile2=open(f'results/{filename2}.txt')
    lines2=graphfile2.readlines()
    x2 = []
    y2 = []
    for line in lines2:
        parts=(line.strip()).split(" ")
        x2.append(int(parts[0]))
        y2.append(float(parts[1]))

    matplotlib.pyplot.plot(x1, y1, label=filename1)
    matplotlib.pyplot.plot(x2, y2, label=filename2)
    matplotlib.pyplot.xlabel('no of IPs')
    matplotlib.pyplot.ylabel('time taken')
    matplotlib.pyplot.title(title)
    matplotlib.pyplot.legend()
    matplotlib.pyplot.show()

i=1
genarategraph(f"ip-insert-radix-{i}",f"ip-insert-trie-{i}","inserting")
genarategraph(f"ip-search-radix-{i}",f"ip-search-trie-{i}","searching")
genarategraph(f"ip-lpm-radix-{i}",f"ip-lpm-trie-{i}","lookup")
genarategraph(f"ip-delete-radix-{i}",f"ip-delete-trie-{i}","deletion")