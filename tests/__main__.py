'''Title: test.py (__main__)
Author(s): Clayton Bennett
Created: 23 March 2025'''
import argparse
class Test():
    devprint = True # change it here, or addd a config ile upon program maturity in sic month (target: 23 September 2025)
    known_instances = {}
    
    @classmethod
    def reset(cls):
        cls.devprint = True
        cls.known_instances = {}
    
    @classmethod
    def add_to_known_instances(cls,key,classinstance_object): 
        cls.known_instances.update({key:classinstance_object})
        
    def print_description(self):
        print(f"Do not instantiate the Test class: \n{self.description}")
    
    @classmethod    
    def devprint(cls):
        "This function calls the class value of devprint, to see if the dev comments should be printed"
        "if Test.devprint()" # bool
        return cls.devprint 
    """
    def __init__(self,key): # If this errors, good - the instances are not supposed to be generated.
        self.key = key
        self.description = "Test is meant to be called as a library / class: Test.devprint() [bool] \nTest is not designed to be run as an instance, like test_object = Test()."
        self.add_to_known_instances(key = self.key, classinstance_object = self)
        self.print_description() """
    @staticmethod
    def do_foo(spare1,script=None):
        print("foo")

    @staticmethod
    def script(script):
        # " Not like this"
        Print.nonprint("test_object = Test(key)")
        Print.nonprint("or")
        Print.nonprint("test_object = Test()")

        # "Like this"
        if Test.devprint():
            print(f"Test.devprint() = {Test.devprint()}") 
        elif not(Test.devprint()):
            print(f"Test.devprint() is False.")

    def main():
        #defaults = config_utils.load_defaults('config.toml')
        defaults = {"devprint":Test.devprint(), "desc":False, "spare":"spare", "foo": False}
        parser = argparse.ArgumentParser(description="Trim an audio file.")
        parser.add_argument("--spare", type=str, default=defaults['spare'], help="spare")
        parser.add_argument("-f","--foo", type=bool, default=defaults['foo'], help="foo")
        parser.add_argument("-d", "--devprint", type=bool, default=defaults['devprint'], help="Test.devprint()")
        parser.add_argument("-desc", "--description", type=bool, default=defaults['desc'], help="Test.print_description()")
        parser.add_argument("-s","--script", action="store_true", help="Run Test.script()")
        
        args = parser.parse_args()
        if args.foo:
            Test.do_foo(vars(args),script=None)
        elif args.devprint is not None:
            Test.devprint()
        else:
            Test.script(args.script)



class Print:
    @staticmethod
    def nonprint(line):
        "nonprint"
        #print(line)
        pass


if __name__ == "__main__":
    if False:
        Test.script()
            

    elif False:
        app = Test()
        app.onecmd_plus_hooks("test")
        app.reset()
        app.cmdloop()

    else:
        Test.main()
