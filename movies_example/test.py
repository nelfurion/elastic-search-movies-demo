from threading import Timer

def twoArgs(arg1,arg2):
    Timer(1.0, twoArgs, ("arg1", "arg2")).start()

def nArgs(*args):
    for each in args:
        print (each)

#arguments:
#how long to wait (in seconds),
#what function to call,
#what gets passed in
r = Timer(1.0, twoArgs, ("arg1","arg2"))
s = Timer(2.0, nArgs, ("OWLS","OWLS","OWLS"))

r.start()
s.start()