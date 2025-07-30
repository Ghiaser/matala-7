from contiguous_labeling import contiguous_oriented_labeling

class FastGraphicalCakeDivider:
    def __init__(self, graph, edge_values):
        """
        graph: networkx.Graph object
        edge_values: list of two dicts [{edge: value}, {edge: value}] representing valuations of two agents
        """
        self.graph = graph
        self.edge_values = edge_values

    def divide(self):
        # מקבל את התווית המכילה: (label, i_minus, i_plus)
        directed_edges = contiguous_oriented_labeling(self.graph)

        A, B = [], []
        value_A, value_B = 0.0, 0.0

        # לולאה על שלושה פריטים בכל איבר ברשימה
        for _, u, v in directed_edges:
            edge = (min(u, v), max(u, v))  # קשת בלתי מכוונת לפי הסכמה
            val0 = self.edge_values[0].get(edge, 0)
            val1 = self.edge_values[1].get(edge, 0)

            # מחלקים את הקשת בין שתי הקבוצות לפי הערך המצטבר
            if value_A <= value_B:
                A.append(edge)
                value_A += val0
            else:
                B.append(edge)
                value_B += val1

        return [A, B]
