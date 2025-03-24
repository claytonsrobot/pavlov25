'''
Title: test.py (__main__)
Author(s): Clayton Bennett and Michael Gratzer

'''

class Test:
    logprint = True # change it here, or addd a config ile upon program maturity in sic month (target: 23 September 2025)
    known_instances = {}
    
    def __init__(self,key): # If this errors, good - the instances are not supposed to be generated.
        self.key = key
        self.description = "Test is meant to be called as a library / class: Test.logprint() [bool] \nTest is not designed to be run as an instance, like test_object = Test()."
        self.add_to_known_instances(key = self.key, classinstance_object = self)
        self.print_description()
    @classmethod
    def add_to_known_instances(cls,key,classinstance_object): 
        cls.known_instances.update({key:classinstance_object})
        
    def print_description(self):
        print(f"Do not instantiate the Test class: \n{self.description}")
    
    
    def logprint(cls):
        "if Test.logprint()" # bool
        return cls.logprint 


def foo(line):
    pass
if __name__ == "__main__":
    # " Not like this"
    foo("test_object = Test(key)")
    foo("or")
    foo("test_object = Test()")

    # "Like this"
    if Test.logprint():
        print(f"Test.logprint() = {Test.logprint()}") 
    elif not(Test.logprint()):
        print(f"Test.logprint() is False.")

