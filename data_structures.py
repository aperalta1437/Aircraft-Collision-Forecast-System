import sys

# Create a tree node
class TreeNode(object):
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.height = 1


class AVLTree(object):

    def __init__(self, index):
        self.index = index

    # Function to insert a node
    def insert_node(self, root, key):

        # Find the correct location and insert the node
        if not root:
            return TreeNode(key)
        elif key.data[self.index] < root.key.data[self.index]:
            root.left = self.insert_node(root.left, key)
        else:
            root.right = self.insert_node(root.right, key)

        root.height = 1 + max(self.getHeight(root.left),
                              self.getHeight(root.right))

        # Update the balance factor and balance the tree
        balanceFactor = self.getBalance(root)

        if balanceFactor > 1 and key.data[self.index] < root.left.key.data[self.index]:
            return self.rightRotate(root)

            # Case 2 - Right Right
        if balanceFactor < -1 and key.data[self.index] > root.right.key.data[self.index]:
            return self.leftRotate(root)

            # Case 3 - Left Right
        if balanceFactor > 1 and key.data[self.index] > root.left.key.data[self.index]:
            root.left = self.leftRotate(root.left)
            return self.rightRotate(root)

            # Case 4 - Right Left
        if balanceFactor < -1 and key.data[self.index] < root.right.key.data[self.index]:
            root.right = self.rightRotate(root.right)
            return self.leftRotate(root)

        return root

    # Function to delete a node
    def delete_node(self, root, key):

        # Find the node to be deleted and remove it
        if not root:
            return root
        elif key < root.key:
            root.left = self.delete_node(root.left, key)
        elif key > root.key:
            root.right = self.delete_node(root.right, key)
        else:
            if root.left is None:
                temp = root.right
                root = None
                return temp
            elif root.right is None:
                temp = root.left
                root = None
                return temp
            temp = self.getMinValueNode(root.right)
            root.key = temp.key
            root.right = self.delete_node(root.right,
                                          temp.key)
        if root is None:
            return root

        # Update the balance factor of nodes
        root.height = 1 + max(self.getHeight(root.left),
                              self.getHeight(root.right))

        balanceFactor = self.getBalance(root)

        # Balance the tree
        if balanceFactor > 1:
            if self.getBalance(root.left) >= 0:
                return self.rightRotate(root)
            else:
                root.left = self.leftRotate(root.left)
                return self.rightRotate(root)
        if balanceFactor < -1:
            if self.getBalance(root.right) <= 0:
                return self.leftRotate(root)
            else:
                root.right = self.rightRotate(root.right)
                return self.leftRotate(root)
        return root

    # Function to perform left rotation
    def leftRotate(self, z):
        y = z.right
        T2 = y.left
        y.left = z
        z.right = T2
        z.height = 1 + max(self.getHeight(z.left),
                               self.getHeight(z.right))
        y.height = 1 + max(self.getHeight(y.left),
                               self.getHeight(y.right))
        return y

    # Function to perform right rotation
    def rightRotate(self, z):
        y = z.left
        T3 = y.right
        y.right = z
        z.left = T3
        z.height = 1 + max(self.getHeight(z.left),
                                self.getHeight(z.right))
        y.height = 1 + max(self.getHeight(y.left),
                                self.getHeight(y.right))
        return y

    # Get the height of the node
    def getHeight(self, root):
        if not root:
            return 0
        return root.height

    # Get balance factore of the node
    def getBalance(self, root):
        if not root:
            return 0
        return self.getHeight(root.left) - self.getHeight(root.right)

    def getMinValueNode(self, root):
        if root is None or root.left is None:
            return root
        return self.getMinValueNode(root.left)

    def preOrder(self, root):
        if not root:
            return
        print("{0} ".format(root.key.data[self.index]), end="")
        self.preOrder(root.left)
        self.preOrder(root.right)


    def print_in_order(self, key):
        """
        Prints the values of the list in order, with the
        left child first, the parent second, and the right child third.
        :return: None
        """
        if self is None:
            return
        else:
            if self.lChild is not None:
                self.lChild.print_in_order()
            print(self.data, end=', ')
            if self.rChild is not None:
                self.rChild.print_in_order()

    # Print the tree
    def printHelper(self, currPtr, indent, last):
        if currPtr != None:
            sys.stdout.write(indent)
            if last:
                sys.stdout.write("R----")
                indent += "     "
            else:
                sys.stdout.write("L----")
                indent += "|    "
            print(currPtr.key.data[self.index])
            self.printHelper(currPtr.left, indent, False)
            self.printHelper(currPtr.right, indent, True)

    def get_node(self, root, look_up_val):
        if not root:
            return
        elif look_up_val == root.key.data[self.index][:len(look_up_val)]:
            return root
        else:
            if look_up_val < root.key.data[self.index][:len(look_up_val)]:
                return self.get_node(root.left, look_up_val)
            else:
                return self.get_node(root.right, look_up_val)

    def get_in_order_list(self, root, text_input):
        similar_node = self.get_node(root, text_input)

        if similar_node is None:
            return None

        airports_list = self.get_first_ten(similar_node, text_input)
        airports_list.sort(key=lambda data_ref: data_ref[self.index])

        return airports_list[:10]

    def get_first_ten(self, root, text_input):

        if root is None or text_input != root.key.data[self.index][:len(text_input)]:
            return []
        else:
            return [root.key.data] + self.get_first_ten(root.left, text_input) + self.get_first_ten(root.right, text_input)







