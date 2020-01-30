class HT_Node(object):
    def __init__(self, label, sc):
        self.label = label
        self.support_count = sc
        self.next_node = None
