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
        self.children,
        self.level) = (None, None, None, [], -1)

    def set_item_attrs(self,
                 parent_item=None,
                 previous_item=None,
                 next_item=None,
                 children=None):
        self.set_parent_item(parent_item)
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
        t2.set_parent_item(t1)

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
        else:
            tree1, bot1, next1 = self, self.children[pos-1].get_tree_bottom_item(), self.children[pos]
            tree2, bot2, next2 = item.get_tree_bot_next()

        tree1.children.insert(pos, item)
        self.fix_links(tree1, bot1, next1,
                       tree2, bot2, next2)

    def insert_after(self, item, sibling):
        try:
            pos = self.children.index(sibling)
        except ValueError:
            logging.exception("sibling not found in children")

        self.insert_tree(item, pos+1)

    def remove_child_tree(self, child):
        try:
            pos = self.children.index(child)
        except ValueError:
            logging.exception("item %s not found in children", child)

        prev1 = child.previous_item
        next1 = child.get_tree_next_item()

        prev1.next_item = next1
        if next1 is not None:
            next1.previous_item = prev1
        self.children.pop(pos)

    def remove_tree_from_parent(self):
        parent = self.get_parent_item()
        parent.remove_child_tree(self)

    def get_tree_bottom_item(self):
        """ return the bottom element of a tree """
        if len(self.children) > 0:
            return self.children[-1].get_tree_bottom_item()
        return self

    def get_tree_next_item(self):
        bot = self.get_tree_bottom_item()
        return bot.next_item

    def get_siblings_after_item(self, item):
        pos = self.get_child_pos(item)
        return self.children[pos+1:]


    def get_tree_bot_next(self):
        """ get the tree root, tree bottom, and the next of the bottom items """
        bot_item = self.get_tree_bottom_item()
        return self, bot_item, bot_item.next_item

    def get_child_count(self):
        return len(self.children)

    def get_child_pos(self, child):
        try:
            pos = self.children.index(child)
        except ValueError:
            logging.exception("Item %s not found in parent's children", child)
            raise
        return pos

    def get_parent_item(self):
        return self.parent_item

    def set_parent_item(self, parent_item):
        self.parent_item = parent_item
        self.adjust_indent_level()

    def delete_item_from_tree(self):
        pos = self.parent_item.get_child_pos(self)
        bottom = self.get_tree_bottom_item()

        # parent, prev, next, children
        self.parent_item.children.remove(self)
        self.previous_item.next_item = bottom.next_item

        if bottom.next_item is not None:
            bottom.next_item.previous_item = self.previous_item

        for child in reversed(self.children):
            self.parent_item.insert_tree(child, pos)

    def get_prev_item_at_same_level(self):
        clevel = self.level
        prev_item = self.previous_item
        while prev_item is not None:
            if prev_item.level < clevel:
                return None
            if prev_item.level == clevel:
                return prev_item
            prev_item = prev_item.previous_item
        return None

    def print_tree(self):
        if hasattr(self, "text"):
            print self.text
        else:
            print "HEAD"
        if self.next_item is not None:
            self.next_item.print_tree()

    def adjust_level(self):
        self.level = self.get_parent_item().level + 1
        return self.level

    def get_children(self):
        return self.children

    def get_all_children(self):
        all_children = self.children[:]
        for child in self.children:
            all_children.extend(child.get_all_children())
        return all_children

    def test_tree(self):
        # parent child
        print "now testing %s%s" % ("  " * self.level, str(self))
        tab = "    "

        try:
            assert self in self.parent_item.children
        except:
            print tab + "Child %s not in parent %s's children" % (self, self.parent_item)

        try:
            assert self == self.previous_item.next_item
        except:
            print tab + "Item %s is not next of previous %s but %s is next" % (self,
                                                                       self.previous_item,
                                                                       self.previous_item.next_item)
        if self.next_item is not None:
            try:
                assert self.next_item.previous_item == self
            except:
                print tab + "Item %s is not previous of next %s but %s is previous" % (self,
                                                                           self.next_item,
                                                                           self.next_item.previous_item)

        for child in self.children:
            child.test_tree()

