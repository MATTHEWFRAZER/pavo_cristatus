import gzip

#TODO: find a more optimal means of compressing data
def compress(data):
    return data#gzip.compress(data)

def decompress(data):
    return data#gzip.decompress(data)