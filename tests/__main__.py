'''
Title: test.py (__main__)
Author(s): Clayton Bennett and Michael Gratzer

'''

class Test:
    devprint = True # change it here, or addd a config ile upon program maturity in sic month (target: 23 September 2025)
    known_instances = {}
    
    @classmethod
    def reset(cls):
        cls.devprint = True
        cls.known_instances = {}
    
    def __init__(self,key): # If this errors, good - the instances are not supposed to be generated.
        self.key = key
        self.description = "Test is meant to be called as a library / class: Test.devprint() [bool] \nTest is not designed to be run as an instance, like test_object = Test()."
        self.add_to_known_instances(key = self.key, classinstance_object = self)
        self.print_description()
    @classmethod
    def add_to_known_instances(cls,key,classinstance_object): 
        cls.known_instances.update({key:classinstance_object})
        
    def print_description(self):
        print(f"Do not instantiate the Test class: \n{self.description}")
    
    
    def devprint(cls):
        "This function calls the class value of devprint, to see if the dev comments should be printed"
        "if Test.devprint()" # bool
        return cls.devprint 

class Print:
    @staticmethod
    def nonprint(line):
        "nonprint"
        #print(line)
        pass

if __name__ == "__main__":
    # " Not like this"
    Test.nonprint("test_object = Test(key)")
    Test.nonprint("or")
    Test.nonprint("test_object = Test()")

    # "Like this"
    if Test.devprint():
        print(f"Test.devprint() = {Test.devprint()}") 
    elif not(Test.devprint()):
        print(f"Test.devprint() is False.")

