from SerialProcessor import SerialProcessor
from multiprocessing import Process

def main():
    sp = SerialProcessor('COM6', 9600, 'test')
    sp.go()

if __name__ == "__main__":
    main()