import gzip

#TODO: find a more optimal means of compressing data
def compress(data : str) -> str:
    return data#gzip.compress(data)

def decompress(data : str) -> str:
    return data#gzip.decompress(data)