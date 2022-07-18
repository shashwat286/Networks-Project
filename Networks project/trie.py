import textwrap


class TrieNode:
    def __init__(self):
        self.children = [None]*2
        self.ip = ''
        self.maskbit = 32
        self.isIP = False
        self.data = None

    @property
    def network(self):
        ipArr = textwrap.wrap(self.ip, 8)
        for i in range(len(ipArr)):
            ipArr[i] = str(int(ipArr[i], 2))
        ip = '.'.join(ipArr)
        addArr = [ip, str(self.maskbit)]
        ipAddr = '/'.join(addArr)
        return ipAddr


class Trie:
    def __init__(self):
        self.root = TrieNode()
        self.root.ip = '0'*32
        self.root.maskbit = 0
        self.nodeCount = 0

    def _ip_to_binary(self, ip):
        ip = ip.split('.')
        ipString = ''
        for i in range(4):
            ipString += '{0:08b}'.format(int(ip[i]))
        return ipString

    def _generate_mask(self, maskbit):
        res = []
        for i in range(maskbit):
            res.append('1')
        for i in range(32 - maskbit):
            res.append('0')
        return ''.join(res)

    def _char_to_index(self, ch):
        return ord(ch)-ord('0')

    def height(self, node):
        x, y = 0, 0
        if node.children[0] is not None:
            x = 1 + self.height(node.children[0])
        if node.children[1] is not None:
            y = 1 + self.height(node.children[1])
        if not node.children[0] and node.children[1]:
            return 0
        return max(x, y)

    def add(self, key):
        splitup = key.split('/')
        if len(splitup) == 1:
            maskbit = 32
        else:
            maskbit = int(splitup[1])
        ipadd = self._ip_to_binary(splitup[0])
        node = self.root

        for level in range(maskbit):
            index = self._char_to_index(ipadd[level])
            mask = self._generate_mask(level + 1)

            if not node.children[index]:
                node.children[index] = TrieNode()
                node.children[index].ip = str(
                    bin(int(ipadd, 2) & int(mask, 2)).replace('0b', '')).rjust(32, '0')
                node.children[index].maskbit = level + 1

            node = node.children[index]

        node.isIP = True
        node.data = {}
        self.nodeCount = maskbit
        return node

    def search(self, key):
        splitup = key.split('/')

        if len(splitup) == 1:
            maskbit = 32
        else:
            maskbit = int(splitup[1])

        ipadd = self._ip_to_binary(splitup[0])
        node = self.root
        level = 0

        while(level < maskbit):
            index = self._char_to_index(ipadd[int(level)])
            level += 1
            if not node.children[int(index)]:
                self.nodeCount = level
                return None
            node = node.children[int(index)]

        self.nodeCount = level
        if node != None and node.isIP:
            return node

    def _delete(self, node, ipAddr, maskBit):
        self.nodeCount += 1
        length = len(ipAddr)
        if maskBit + length == 32:
            for i in range(2):
                if node.children[i] != None:
                    if node.isIP == False:
                        raise KeyError("IP not present")
                    node.isIP = False
                    return False

            del node
            return True
        else:
            index = self._char_to_index(ipAddr[0])
            if(node.children[index] == None):
                raise KeyError("IP not present")
            done = self._delete(node.children[index], ipAddr[1:], maskBit)

            if done == True:
                node.children[index] = None

                for i in range(2):
                    if node.children[i] != None:
                        return False

                del node
                return True
            return False

    def longest_prefix_match(self, key):
        key = self._ip_to_binary(key)
        stack = None
        node = self.root
        i = 0
        while (i < 32):
            index = self._char_to_index(key[int(i)])
            if not node.children[int(index)]:
                break
            node = node.children[int(index)]
            if node.isIP:
                stack=node
            i += 1

        self.nodeCount = i
        if stack:
            return stack

        return None

    def delete(self, key):
        self.nodeCount = 0
        splitup = key.split('/')
        if len(splitup) == 1:
            maskbit = 32
        else:
            maskbit = int(splitup[1])
        ipadd = self._ip_to_binary(splitup[0])

        self._delete(self.root, ipadd, maskbit)


def main():
    tree = Trie()
    node1 = tree.add('1.2.3.4/24')
    node2 = tree.add('1.2.3.5/16')
    node4=tree.add('1.1.3.2/12')
    node3 = tree.longest_prefix_match('1.1.1.4')
    print(node3.network)


if __name__ == '__main__':
    main()
