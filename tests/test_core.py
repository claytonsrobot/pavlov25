'''Title: test.py (__main__)
Author(s): Clayton Bennett
Created: 23 March 2025'''
import argparse

class Print:
    @staticmethod
    def nonprint(line):
        "nonprint"
        #print(line)
        pass

class Test():
    devprint_bool = True # change it here for now, or add a config file upon program maturity in six month (target: 23 September 2025)
    description = "Test is meant to be called as a class: Test.get_devprint()\nTest is not designed to be run as an instance."
    #known_instances = {} 
    
    @classmethod
    def reset(cls):
        devprint_bool = True
        #cls.known_instances = {}
    
    #@classmethod
    #def add_to_known_instances(cls,key,classinstance_object): 
    #    cls.known_instances.update({key:classinstance_object})
    @classmethod
    def print_description(cls):
        print(f"{cls.description}")
    
    @classmethod
    def get_devprint(cls):
        "This function calls the class value of devprint, to see if the dev comments should be printed"
        "if Test.get_devprint()" # bool
        return cls.devprint_bool 
    
    #def __init__(self,key): # If this errors, good - the instances are not supposed to be generated.
    #    super().__init__()
    #    self.key = key
    #    self.add_to_known_instances(key = self.key, classinstance_object = self)

    @staticmethod
    def status(script_var=None):
        print("Running Test.status(None)...")

        # " Not like this"
        Print.nonprint("test_object = Test(key)")
        Print.nonprint("or")
        Print.nonprint("test_object = Test()")

        # "Like this"
        if Test.get_devprint():
            print(f"Test.get_devprint() = {Test.get_devprint()}") 
        elif not(Test.get_devprint()):
            print(f"Test.get_devprint() is False.")

    def get(args=None,print_result=False): # print_result should be true if you want to be able to apply a variable in powershell
        "Test.main(['-d'])  # Simulates 'python -m tests -d'"  
        parser = argparse.ArgumentParser(description="Explore the Test class functionionality.")
        parser.add_argument("-d", "--devprint", action="store_true", help="Test.get_devprint()")
        parser.add_argument("-desc", "--description", action="store_true", help="Test.print_description()")
        args = parser.parse_args(args)

        if args.description:
            Test.print_description()
        elif args.devprint:
            result = Test.get_devprint()
            if print_result:
                print(result) # leave this here, for powershell var assignment. This should be the onl print statement.
            return result
        else:
            args = parser.parse_args(["-h"])  # Display help if no arguments are provided.
if __name__ == "__main__":
    Test.get(print_result=True)
