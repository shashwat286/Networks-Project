import time

import radix
import trie

def performance(tree, i, name):

    def insertions():
        ipFile = open(f'datasets/ip-insert-{i}.txt')
        ipList = ipFile.read().splitlines()
        opFile = open(f'results/ip-insert-{name}-{i}.txt','w')
        nodecount = 0
        start = time.time()
        b=0
        for ip in ipList:
            b+=1
            tree.add(ip)
            nodecount += tree.nodeCount
            end = time.time()
            opFile.write(f'{b} {end-start}\n')

        nodecount /= len(ipList)
        print(f'Insertion time for {len(ipList)} IPs: {end - start}. Mean number of node traversals: {nodecount}')

    def deletions():
        ipFile = open(f'datasets/ip-insert-{i}.txt')
        ipList = ipFile.read().splitlines()
        opFile = open(f'results/ip-delete-{name}-{i}.txt','w')
        nodecount = 0
        start = time.time()
        b=0
        for ip in ipList:
            b+=1
            try:
                tree.delete(ip)
            except:
                pass
            nodecount += tree.nodeCount
            end = time.time()
            opFile.write(f'{b} {end-start}\n')

        nodecount /= len(ipList)
        print(f'Deletion time for inserted IPs: {end - start}. Mean number of node traversals: {nodecount}')

    def searches():
        ipFile = open(f'datasets/ip-search-{i}.txt')
        ipList = ipFile.read().splitlines()
        opFile = open(f'results/ip-search-{name}-{i}.txt','w')
        nodecount = 0
        start = time.time()
        b=0
        for ip in ipList:
            b+=1
            tree.search(ip)
            nodecount += tree.nodeCount
            end = time.time()
            opFile.write(f'{b} {end-start}\n')

        end = time.time()
        nodecount /= len(ipList)
        print(f'Searching time for {len(ipList)} IPs: {end - start}. Mean number of node traversals: {nodecount}')

    def longest_prefix_matches():
        ipFile = open(f'datasets/ip-lpm-{i}.txt')
        ipList = ipFile.read().splitlines()
        opFile = open(f'results/ip-lpm-{name}-{i}.txt','w')
        nodecount = 0
        start = time.time()
        b=0
        for ip in ipList:
            b+=1
            tree.longest_prefix_match(ip)
            nodecount += tree.nodeCount
            end = time.time()
            opFile.write(f'{b} {end-start}\n')

        end = time.time()
        nodecount /= len(ipList)
        print(f'Longest prefix match time for {len(ipList)} IPs: {end - start}. Mean number of node traversals: {nodecount}')

    insertions()
    searches()
    longest_prefix_matches()
    deletions()

for i in range(1, 5):
    print(f'\n\nDataset {i}:')
    print('\nPerformance in radix tree:')
    performance(radix.Radix(), i, "radix")
    print('\nPerformance in trie:')
    performance(trie.Trie(), i, "trie")
