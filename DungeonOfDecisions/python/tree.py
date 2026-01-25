class DecisionNode:
    def __init__(self, description):
        self.description = description
        self.left = None
        self.right = None


def build_decision_tree():
    root = DecisionNode("¿Pelear o huir?")
    root.left = DecisionNode("Pelear")
    root.right = DecisionNode("Huir")
    root.left.left = DecisionNode("Atacar")
    root.left.right = DecisionNode("Defender")
    return root
