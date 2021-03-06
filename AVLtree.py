class BSTNode:
    def __init__(self, value):
        self.parent = None
        self.value = value
        self.left = None
        self.right = None
        self.left_count = 0
        self.right_count = 0

    def update_from_childs(self):
        l_count = 0
        r_count = 0
        if self.left is not None:
            l_count = self.left.left_count + self.left.right_count + 1
        if self.right is not None:
            r_count = self.right.left_count + self.right.right_count + 1
        self.left_count = l_count
        self.right_count = r_count
        return


class BST:
    def __init__(self):
        self.root = None
        self.size = 0

    def push(self, value):
        self.size += 1
        if self.root is None:
            self.root = BSTNode(value)
            return
        actual = self.root
        child = None
        while True:
            if value > actual.value:
                if actual.right is not None:
                    actual = actual.right
                else:
                    # create child node
                    child = BSTNode(value)
                    # append node
                    actual.right = child
                    child.parent = actual
                    break
            else:
                if actual.left is not None:
                    actual = actual.left
                else:
                    # create child node
                    child = BSTNode(value)
                    # append node
                    actual.left = child
                    child.parent = actual
                    break

        # child can do something with counts
        actual = child
        while actual is not None:
            actual.update_from_childs()
            actual = actual.parent


class InvalidCastException(Exception):
    def __init__(self):
        super().__init__(self)


class AVLNode(BSTNode):
    def __init__(self, value):
        super().__init__(value)
        self.left_depth = 0
        self.right_depth = 0

    def update_from_childs(self):
        super().update_from_childs()
        l_depth = 0
        r_depth = 0
        if self.left is not None:
            l_depth = max(self.left.left_depth, self.left.right_depth) + 1
        if self.right is not None:
            r_depth = max(self.right.left_depth, self.right.right_depth) + 1
        self.left_depth = l_depth
        self.right_depth = r_depth

    def get_balance_factor(self):
        return self.left_depth - self.right_depth


class AVL(BST):
    def __init__(self):
        super().__init__()

    def left_rotation(self, new_subroot):
        # check if not root
        # then cannot rotate
        if new_subroot.parent is None:
            raise InvalidCastException()
        parent = new_subroot.parent.parent
        left = new_subroot.parent
        left_right = new_subroot.left
        new_subroot.parent = parent
        if parent is not None:
            if parent.left == left:
                parent.left = new_subroot
            elif parent.right == left:
                parent.right = new_subroot
            else:
                assert False
        if left_right is not None:
            left_right.parent = left
        left.right = left_right
        left.parent = new_subroot
        new_subroot.left = left
        left.update_from_childs()
        new_subroot.update_from_childs()
        if new_subroot.parent is None:
            self.root = new_subroot
        return

    def right_rotation(self, new_subroot):
        # check if not root
        # then cannot rotate
        if new_subroot.parent is None:
            raise InvalidCastException()
        parent = new_subroot.parent.parent
        right = new_subroot.parent
        right_left = new_subroot.right
        new_subroot.parent = parent
        if parent is not None:
            if parent.left == right:
                parent.left = new_subroot
            elif parent.right == right:
                parent.right = new_subroot
        if right_left is not None:
            right_left.parent = right
        right.left = right_left
        right.parent = new_subroot
        new_subroot.right = right
        right.update_from_childs()
        new_subroot.update_from_childs()
        if new_subroot.parent is None:
            self.root = new_subroot
        return

    def push(self, value):
        self.size += 1
        if self.root is None:
            self.root = AVLNode(value)
            return
        actual = self.root
        child = None
        while True:
            if value > actual.value:
                if actual.right is not None:
                    actual = actual.right
                else:
                    # create child node
                    child = AVLNode(value)
                    # append node
                    actual.right = child
                    child.parent = actual
                    break
            else:
                if actual.left is not None:
                    actual = actual.left
                else:
                    # create child node
                    child = AVLNode(value)
                    # append node
                    actual.left = child
                    child.parent = actual
                    break

        # child can do something with counts
        actual = child
        while actual is not None:
            actual.update_from_childs()
            if actual.get_balance_factor() == 2:
                if actual.left.get_balance_factor() == -1:
                    self.left_rotation(actual.left.right)
                self.right_rotation(actual.left)
            elif actual.get_balance_factor() == -2:
                if actual.right.get_balance_factor() == 1:
                    self.right_rotation(actual.right.left)
                self.left_rotation(actual.right)
            else:
                actual = actual.parent


class MyAVLNode(AVLNode):
    def __init__(self, value, nationality, nations):
        super().__init__(value)
        self.number_of_overruns = 0
        self.nationality = nationality
        self.nations = nations
        self.nationalities_overruns = {}
        self.nations_left = {}
        self.nations_right = {}
        for nat in nations:
            self.nationalities_overruns[nat] = 0
            self.nations_left[nat] = 0
            self.nations_right[nat] = 0

    def update_from_childs(self):
        super().update_from_childs()
        for nat in self.nations:
            # erase value
            self.nations_left[nat] = 0
            self.nations_right[nat] = 0
            if self.left is not None:
                self.nations_left[nat] = self.left.nations_left[nat]\
                                         + self.left.nations_right[nat]
                if self.left.nationality == nat:
                    self.nations_left[nat] += 1
            if self.right is not None:
                self.nations_right[nat] = self.right.nations_left[nat]\
                                          + self.right.nations_right[nat]
                if self.right.nationality == nat:
                    self.nations_right[nat] += 1


class MyAVL(AVL):
    def __init__(self, nations):
        super().__init__()
        self.nations = nations

    def push(self, value, nationality):
        self.size += 1
        if self.root is None:
            self.root = MyAVLNode(value, nationality, self.nations)
            return
        actual = self.root
        child = None
        overruns = 0
        nation_overruns = {}
        for nat in self.nations:
            nation_overruns[nat] = 0
        while True:
            if value > actual.value:
                # add overruns
                overruns += actual.left_count + 1
                for nat in self.nations:
                    nation_overruns[nat] += actual.nations_left[nat]
                nation_overruns[actual.nationality] += 1
                if actual.right is not None:
                    actual = actual.right
                else:
                    # create child node
                    child = MyAVLNode(value, nationality, self.nations)
                    child.number_of_overruns = overruns
                    child.nationalities_overruns = nation_overruns
                    # append node
                    actual.right = child
                    child.parent = actual
                    break
            else:
                if actual.left is not None:
                    actual = actual.left
                else:
                    # create child node
                    child = MyAVLNode(value, nationality, self.nations)
                    child.number_of_overruns = overruns
                    child.nationalities_overruns = nation_overruns
                    # append node
                    actual.left = child
                    child.parent = actual
                    break

        # child can do something with counts
        actual = child
        while actual is not None:
            actual.update_from_childs()
            if actual.get_balance_factor() == 2:
                if actual.left.get_balance_factor() == -1:
                    self.left_rotation(actual.left.right)
                self.right_rotation(actual.left)
            elif actual.get_balance_factor() == -2:
                if actual.right.get_balance_factor() == 1:
                    self.right_rotation(actual.right.left)
                self.left_rotation(actual.right)
            else:
                actual = actual.parent

    def go_through_all(self, subroot, result):
        if subroot is None:
            return (0, result)
        for nat in self.nations:
            sn = subroot.nationality
            result[sn][nat] += subroot.nationalities_overruns[nat]
        return (
            subroot.number_of_overruns +
            self.go_through_all(subroot.left, result)[0] +
            self.go_through_all(subroot.right, result)[0],
            result)


def make_statistics_n2(results):
    nationalities = {}
    for r in results:
        nationalities[r[1]] = True
    nations = list(nationalities)
    numres = 0
    result = {}
    # fill result with zeros
    for n in nations:
        result[n] = {}
        for nat in nations:
            result[n][nat] = 0
    i = 0
    while i < len(results):
        j = i + 1
        while j < len(results):
            if results[i][0] > results[j][0]:
                numres += 1
                result[results[i][1]][results[j][1]] += 1
            j += 1
        i += 1
    return numres, result


def make_statistics(results):
    # if problem occured try uncomment following line
    # return make_statistics_n2(results)
    return make_stats(results)


def make_stats(results):
    """ makes statistics in n log n """
    """
    adds runners from last to modified AVL tree (sorted by number)
    runners at left are overruned
    then sums values
    """
    nationalities = {}
    for r in results:
        nationalities[r[1]] = True
    nations = list(nationalities)

    result = {}
    # fill result with zeros
    for n in nations:
        result[n] = {}
        for nat in nations:
            result[n][nat] = 0

    i = len(results) - 1
    tree = MyAVL(nations)
    while i >= 0:
        tree.push(results[i][0], results[i][1])
        i -= 1
    return tree.go_through_all(tree.root, result)


if __name__ == "__main__":
    input = [
        (1, 'CZ'),
        (9, 'FR'),
        (5, 'EN'),
        (7, 'EN'),
        (6, 'CZ'),
        (4, 'EN'),
        (8, 'CZ'),
        (2, 'CZ'),
        (3, 'EN')
        ]
    print(make_statistics(input))
