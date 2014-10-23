from unsalted_hash_crack import *

def main():
    
    total = 100000
    start = 0
    
    while start + 1000 <= total:
        salted_crack_aps.delay(start, start+10)
        start = start + 1000

if __name__ == "__main__":
    main()

