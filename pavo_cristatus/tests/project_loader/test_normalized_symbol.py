# normalized symbol works with no parent symbol

# normalized symbol works with parent symbol

# normalized symbol can normalize nested symbols

# normalized symbol can normalize decorated symbol

# normalized symbol can normalize this case:
# need to handle the case where we overwrite symbols in namespace
# example:
# def x():
#       class a: pass
#       def a(): pass
# we should resolve function a

# normalized symbol raises exception if normalized parent is provided without normalized name

# symbol to normalize with no nested symbol raises error

# single line symbol raises error

