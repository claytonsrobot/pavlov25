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
    def do_foo(spare1,spare2):
        print("foo")

    def script(in1, in2, in3):
        # Load the audio file
        audio_data, sample_rate = audio_utils.load_audio(path_in)
        
        # Trim the audio
        trimmed_audio = audio_utils.trim_audio(audio_data, sample_rate, time_start, time_end)

        # Save the trimmed file
        audio_utils.save_audio(path_out, trimmed_audio, sample_rate)

        # Confirmation messaging
        print("Success.")

    def main():
        #defaults = config_utils.load_defaults('config.toml')
        defaults = {key:,:,:}
        parser = argparse.ArgumentParser(description="Trim an audio file.")
        parser.add_argument("-i1", "--input_file", type=str, default=defaults['in1'], help="spare")
        parser.add_argument("-i2", "--output_file", type=str, default=defaults['in2'], help="spare")
        parser.add_argument("-i3", "--start_time", type=float, default=defaults['in3'], help="spare")
        parser.add_argument("--gui", action="store_true", help="Launch the GUI")
        
        args = parser.parse_args()
        if args.foo:
            Test.do_foo(vars(args),script=None)
        else:
            script(args.input_file, args.output_file, args.start_time, args.end_time)



class Print:
    @staticmethod
    def nonprint(line):
        "nonprint"
        #print(line)
        pass



if False:
    if __name__ == "__main__":
        # " Not like this"
        Print.nonprint("test_object = Test(key)")
        Print.nonprint("or")
        Print.nonprint("test_object = Test()")

        # "Like this"
        if Test.devprint():
            print(f"Test.devprint() = {Test.devprint()}") 
        elif not(Test.devprint()):
            print(f"Test.devprint() is False.")

elif False:
    if __name__=='not__main__':
        app = Test()
        app.onecmd_plus_hooks("test")
        app.reset()
        app.cmdloop()

else:
    main()
