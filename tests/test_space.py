from deeper import Isometry, Block

child = Block(Isometry(0, 1, 2))
block = Block(Isometry())
block.add_child(child)
print(block.children)