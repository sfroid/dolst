"""
Doubly linked linear tree

    { sfroid : 2014 }

"""

import logging


class DoublyLinkedLinearTree(object):
    """ Mixin having features of a linear tree and double linked list """
    def __init__(self):
        (self.parent_item,
         self.previous_item,
         self.next_item,
         self.children,
         self.level) = (None, None, None, [], -1)
        self.instance = None


    def set_instance(self, instance):
        """ set the instance variable """
        from experiments.line_items_panel import LineItemsPanel
        self.instance = instance
        isinstance(self.instance, LineItemsPanel)


    def append_child_tree(self, tree_root):
        """ append an item tree to the end of children """
        tree1, bot1, botnext1 = self.get_tree_bot_next()
        tree2, bot2, botnext2 = tree_root.get_tree_bot_next()

        tree1.children.append(tree_root)

        self.fix_links(tree1, bot1, botnext1,
                       tree2, bot2, botnext2)


    def fix_links(self, tree1, bott1, next1, tree2, bott2, dummy):
        # pylint: disable=too-many-arguments
        # pylint: disable=no-self-use
        """ set the links to maintain the doubly linked tree nature """
        tree2.set_parent_item(tree1)

        bott1.next_item = tree2
        tree2.previous_item = bott1

        bott2.next_item = next1
        if next1 is not None:
            next1.previous_item = bott2


    def insert_tree(self, item, pos):
        """ insert an item tree at the given position in children """
        if ((pos == -1) or
                (pos >= len(self.children)) or
                (len(self.children) == 0)):
            self.append_child_tree(item)
            return

        if pos == 0:
            tree1, bot1, next1 = self, self, self.children[0]
            tree2, bot2, next2 = item.get_tree_bot_next()
        else:
            tree1, bot1, next1 = self, self.children[pos - 1].get_tree_bottom_item(), self.children[pos]
            tree2, bot2, next2 = item.get_tree_bot_next()

        tree1.children.insert(pos, item)
        self.fix_links(tree1, bot1, next1,
                       tree2, bot2, next2)


    def insert_after(self, item, sibling):
        """ insert the item tree after the given child (sibling) """
        try:
            pos = self.children.index(sibling)
        except ValueError:
            logging.exception("sibling not found in children")

        self.insert_tree(item, pos + 1)


    def remove_child_tree(self, child):
        """ remove an item tree - only removes it - does not destroy objects """
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
        """ remove this item from parent """
        parent = self.get_parent_item()
        parent.remove_child_tree(self)


    def get_tree_bottom_item(self):
        """ return the bottom element of a tree """
        if len(self.children) > 0:
            return self.children[-1].get_tree_bottom_item()
        return self


    def get_tree_next_item(self):
        """ get next item of this tree (next of tree's bottom item) """
        bot = self.get_tree_bottom_item()
        return bot.next_item


    def get_siblings_after_item(self, item):
        """ get siblings that come after this one in parent's children list """
        pos = self.get_child_pos(item)
        return self.children[pos + 1:]


    def get_tree_bot_next(self):
        """ get the tree root, tree bottom, and the next of the bottom items """
        bot_item = self.get_tree_bottom_item()
        return self, bot_item, bot_item.next_item


    def get_child_count(self):
        """ get the number of children """
        return len(self.children)


    def get_child_pos(self, child):
        """ get position of child in the children's list """
        try:
            pos = self.children.index(child)
        except ValueError:
            logging.exception("Item %s not found in parent's children", child)
            raise
        return pos


    def get_parent_item(self):
        """ return parent item """
        return self.parent_item


    def set_parent_item(self, parent_item):
        """ set the parent item """
        self.parent_item = parent_item
        self.instance.adjust_indent_level()


    def delete_item_from_tree(self):
        """
        remove only this item from the tree  - but not its children
        """
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
        """ get the previous sibling """
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
        """ print out the tree in a recursive manner """
        if hasattr(self.instance, "text"):
            logging.info(self.instance.text)
        else:
            logging.info("HEAD")
        if self.next_item is not None:
            self.next_item.print_tree()


    def adjust_level(self):
        """ set the level as 1 + level of parent """
        self.level = self.get_parent_item().level + 1
        return self.level


    def get_children(self):
        """ return the children """
        return self.children


    def has_child(self, item):
        """ test if item is a child """
        try:
            dummy = self.children.index(item)
            return True
        except ValueError:
            return False


    def get_all_children(self):
        """ get all items in the tree under this one """
        all_children = self.children[:]
        for child in self.children:
            all_children.extend(child.get_all_children())
        return all_children


    def test_tree(self):
        """ test the tree and doubly linked list nature """
        # parent child
        logging.info("now testing %s%s", "  " * self.level, str(self))
        tab = "    "

        try:
            assert self in self.parent_item.children
        except AssertionError:
            logging.info(tab + "Child %s not in parent %s's children", self, self.parent_item)

        try:
            assert self == self.previous_item.next_item
        except AssertionError:
            logging.info(tab + "Item %s is not next of previous %s but %s is next", self,
                         self.previous_item,
                         self.previous_item.next_item)
        if self.next_item is not None:
            try:
                assert self.next_item.previous_item == self
            except AssertionError:
                logging.info(tab + "Item %s is not previous of next %s but %s is previous", self,
                             self.next_item,
                             self.next_item.previous_item)

        for child in self.children:
            child.test_tree()
