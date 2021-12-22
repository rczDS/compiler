# coding=utf-8

# 非终结符: ASTInternalNode
# 终结符: ASTExternalNode

# 基础节点
class ASTNode:
    def __init__(self, key):
        self.key = str(key)


# 内部节点：key，children
class ASTInternalNode(ASTNode):
    def __init__(self, key, children):
        ASTNode.__init__(self, key)
        self.children = children
        for i in range(len(self.children)):
            if not isinstance(self.children[i], ASTNode):
                self.children[i] = ASTExternalNode(str(self.children[i]), str(self.children[i]))

    def __str__(self):
        return ' '.join(map(str, self.children))


# 外部结点：key, value
class ASTExternalNode(ASTNode):
    def __init__(self, key, value):
        ASTNode.__init__(self, key)
        self.value = str(value)

    def __str__(self):
        return self.value

