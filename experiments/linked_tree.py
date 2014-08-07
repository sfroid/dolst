"""
Doubly linked linear tree

    { sfroid : 2014 }

"""

import logging


class DoublyLinkedLinearTree(object):
    def __init__(self):
        (self.parent_item,
        self.previous_item,
        self.next_item,
        self.children) = (None, None, None, [])

    def set_item_attrs(self,
                 parent_item=None,
                 previous_item=None,
                 next_item=None,
                 children=None):
        self.parent_item = parent_item
        self.previous_item = previous_item
        self.next_item = next_item
        self.children = [] if children is None else children

    def append_child_tree(self, tree_root):
        """ add a tree as a child """
        tree1, bot1, botnext1 = self.get_tree_bot_next()
        tree2, bot2, botnext2 = tree_root.get_tree_bot_next()

        tree1.children.append(tree_root)

        self.fix_links(tree1, bot1, botnext1,
                       tree2, bot2, botnext2)

    def fix_links(self, t1, b1, n1, t2, b2, n2):
        t2.parent_item = t1

        b1.next_item = t2
        t2.previous_item = b1

        b2.next_item = n1
        if n1 is not None:
            n1.previous_item = b2

    def insert_tree(self, item, pos):
        if ((pos == -1) or
            (pos >= len(self.children)) or
            (len(self.children) == 0)):
            self.append_child_tree(item)
            return

        if pos == 0:
            tree1, bot1, next1 = self, self, self.children[0]
            tree2, bot2, next2 = item.get_tree_bot_next()

            tree1.children.insert(pos, item)
        else:
            tree1, bot1, next1 = self, self.children[pos-1], self.children[pos]
            tree2, bot2, next2 = item.get_tree_bot_next()

        self.fix_links(tree1, bot1, next1,
                       tree2, bot2, next2)

    def insert_after(self, item, sibling):
        try:
            pos = self.children.index(sibling)
        except ValueError:
            logging.exception("sibling not found in children")

        self.insert_tree(item, pos+1)

    def get_tree_bottom_item(self):
        """ return the bottom element of a tree """
        if len(self.children) > 0:
            return self.children[-1].get_tree_bottom_item()
        return self

    def get_tree_bot_next(self):
        """
        get the tree root, tree bottom, and the next of the bottom items
        """
        bot_item = self.get_tree_bottom_item()
        return self, bot_item, bot_item.next_item

