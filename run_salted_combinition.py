from unsalted_hash_crack import *

def main():
    
    total = 100000
    start = 0
    
    while start + 5 <= total:
        salted_crack_combinitions.delay(start, start+10)
        start = start + 5

if __name__ == "__main__":
    main()

