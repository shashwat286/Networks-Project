import textwrap
import time


class RadixNode:
    def __init__(self):
        self.children = [None]*2
        self.ip = ''
        self.maskbit = 32
        self.data = None
        self.isIP = False

    @property
    def network(self): # changes "11000000101010000000000100000000" , 30 to "192.168.1.0/30" and put it in the attribute network
        ipArr = textwrap.wrap(self.ip, 8)
        for i in range(len(ipArr)):
            ipArr[i] = str(int(ipArr[i], 2))
        ip = '.'.join(ipArr)
        addArr = [ip, str(self.maskbit)]
        ipAddr = '/'.join(addArr)
        return ipAddr


class Radix:
    def _generate_mask(self, maskbit): # changes 14 into "11111111111111000000000000000000"
        res = []

        for i in range(maskbit):
            res.append('1')

        for i in range(32 - maskbit):
            res.append('0')

        return ''.join(res)

    def __init__(self):
        self.root = RadixNode()
        self.root.ip = '0'*32
        self.root.maskbit = 0
        self.masks = [self._generate_mask(x) for x in range(33)]
        self.nodeCount = 0

    def _ip_to_binary(self, ip): # changes 192.168.1.1 to "11000000101010000000000100000001"
        ip1 = ip
        ip1 = ip1.split('.')

        for i in range(len(ip1)):
            ip1[i] = int(ip1[i])
            ip1[i] = str(bin(ip1[i]).replace('0b', ''))
            ip1[i] = ip1[i].rjust(8, '0')

        ip1 = ''.join(ip1)
        return ip1

    def _binary_to_ip(self, binAdd, maskbit): # changes "11000000101010000000000100000001" , 30 to 192.168.1.1/30
        ipArr = textwrap.wrap(binAdd, 8)

        for i in range(len(ipArr)):
            ipArr[i] = str(int(ipArr[i], 2))

        ip = '.'.join(ipArr)
        addArr = [ip, str(maskbit)]
        ipAddr = '/'.join(addArr)
        return ipAddr

    def _char_to_index(self, ch):
        return ord(ch)-ord('0')

    def height(self, node): # finds height of the tree
        if not node.children[0] and node.children[1]:
            return 0
        x, y = 0, 0
        if node.children[0] is not None:
            x = 1 + self.height(node.children[0])
        if node.children[1] is not None:
            y = 1 + self.height(node.children[1])
        return max(x, y)

    def add(self, key):
        splitup = key.split('/')

        if len(splitup) == 1:
            maskbit = 32
        else:
            maskbit = int(splitup[1])

        ipadd = self._ip_to_binary(splitup[0])
        ipadd = str(bin(int(ipadd, 2) & int(self.masks[maskbit], 2)).replace('0b', '')).rjust(32, '0') # why? makes it like masked ip

        node = self.root
        root = None
        childIndex = 0
        flag = False
        self.nodeCount = 0

        while node.maskbit <= maskbit:
            nmaskbit = node.maskbit
            mask = self.masks[nmaskbit]
            maskedip = str(bin(int(ipadd, 2) & int(mask, 2)).replace('0b', '')).rjust(32, '0')

            if maskedip == node.ip:
                # ip completely matches existing glue node
                if nmaskbit == maskbit:
                    node.isIP = True
                    flag = True
                    break
                index = int(ipadd[nmaskbit])
                # node.maskbit < ip.maskbit
                if node.children[index] is None:
                    node.children[index] = RadixNode()
                    node.children[index].ip = ipadd
                    node.children[index].maskbit = maskbit
                    node.children[index].isIP = True
                    node.children[index].data = {}
                    flag = True
                    break
                root = node
                childIndex = index
                node = node.children[index]
                self.nodeCount += 1

            # ip does not match, create a glue node at differing bit
            # and store children accordingly
            else:
                xor = int(maskedip, 2) ^ int(node.ip, 2)
                xor = str(bin(xor).replace('0b', ''))
                newmaskbit = 32 - len(xor) # helps to find the differing bit
                newmask = self.masks[newmaskbit]
                newipadd = str(bin(int(ipadd, 2) & int(newmask, 2)).replace('0b', '')).rjust(32, '0')
                root.children[childIndex] = RadixNode()
                root.children[childIndex].ip = newipadd
                root.children[childIndex].maskbit = newmaskbit
                root.children[childIndex].children[int(ipadd[newmaskbit])] = RadixNode()
                root.children[childIndex].children[int(ipadd[newmaskbit])].ip = ipadd
                root.children[childIndex].children[int(ipadd[newmaskbit])].maskbit = maskbit
                root.children[childIndex].children[int(ipadd[newmaskbit])].isIP = True
                root.children[childIndex].children[int(ipadd[newmaskbit])].data = {}
                root.children[childIndex].children[1 ^ int(ipadd[newmaskbit])] = node
                flag = True
                break
        # node.maskbit > ip.maskbit
        if not flag:
            mask = self.masks[maskbit]
            maskedip = str(bin(int(node.ip, 2) & int(mask, 2)).replace('0b', '')).rjust(32, '0')

            # if ip has matched till node, then directly insert as child
            if maskedip == ipadd:
                root.children[childIndex] = RadixNode()
                root.children[childIndex].ip = ipadd
                root.children[childIndex].maskbit = maskbit
                root.children[childIndex].isIP = True
                root.children[childIndex].data = {}
                root.children[childIndex].children[int(node.ip[maskbit])] = node

            # create glue node and store left and right accordingly
            else:
                xor = int(maskedip, 2) ^ int(ipadd, 2)
                xor = str(bin(xor).replace('0b', ''))
                if xor == '0':
                    newmaskbit = 0
                else:
                    newmaskbit = 32 - len(xor)
                mask1 = self.masks[newmaskbit]
                ip1 = str(bin(int(ipadd, 2) & int(mask1, 2)).replace('0b', '')).rjust(32, '0')
                root.children[childIndex] = RadixNode()
                root.children[childIndex].ip = ip1
                root.children[childIndex].maskbit = newmaskbit
                root.children[childIndex].children[int(ipadd[newmaskbit])] = RadixNode()
                root.children[childIndex].children[int(ipadd[newmaskbit])].ip = ipadd
                root.children[childIndex].children[int(ipadd[newmaskbit])].maskbit = maskbit
                root.children[childIndex].children[int(ipadd[newmaskbit])].isIP = True
                root.children[childIndex].children[int(ipadd[newmaskbit])].data = {}
                root.children[childIndex].children[1 ^ int(ipadd[newmaskbit])] = node

    def search(self, key):
        self.nodeCount = 0
        splitup = key.split('/')
        if len(splitup) == 1:
            maskbit = 32
        else:
            maskbit = int(splitup[1])
        ipadd = self._ip_to_binary(splitup[0])
        node = self.root
        pmaskbit = node.maskbit

        while pmaskbit < maskbit:
            index = int(ipadd[pmaskbit])
            pchild = node.children[index]
            if not pchild:
                return None
            node = pchild
            self.nodeCount += 1
            pmaskbit = node.maskbit

        if pmaskbit == maskbit and ipadd == node.ip and node.isIP:
            return node
        else:
            return None 

    def _get_parent(self, node):
        key = node.ip
        crawl = self.root
        parent = None
        pmaskbit = crawl.maskbit

        while pmaskbit < node.maskbit:
            index = int(key[pmaskbit])
            crawl, parent = crawl.children[index], crawl
            if crawl == node:
                return parent
            pmaskbit = crawl.maskbit

        return None

    def delete(self, key):
        node = self.search(key)

        if node is None:
            raise KeyError('IP not present')

        node.isIP = False
        node.data = None

        if node.children[0] and node.children[1]:
            return

        child = node.children[0] if node.children[0] else node.children[1]

        if child is not None:
            parent, parentTravel = self._get_parent(node)
            if parent.children[0] == node:
                parent.children[0] = child
            else:
                parent.children[1] = child

        del node

    def longest_prefix_match(self, key):
        key = self._ip_to_binary(key)
        stack = None
        node = self.root
        pmaskbit = node.maskbit
        self.nodeCount = 0

        while pmaskbit < 32:
            index = int(key[pmaskbit])
            if node.isIP and key[:pmaskbit] == node.ip[:pmaskbit]:
                stack = node
            pchild = node.children[index]
            if not pchild:
                break
            node = pchild
            self.nodeCount += 1
            pmaskbit = node.maskbit

        if pmaskbit == 32:
            if node.isIP and key[:32] == node.ip[:32]:
                stack = node

        if stack:
            return stack

        return None


def main():
    tree = Radix()
    tree.add('1.2.3.4/24')
    tree.add('1.2.3.5/16') #add(self, key) key:'1.2.3.5/16'  key.split('/'): ['1.2.3.5', '16']
    #key: "1.2.3.4" split: ["1.2.3.4"]
    node3 = tree.longest_prefix_match('1.2.3.4')
    print(node3.network)


if __name__ == '__main__':
    main()
