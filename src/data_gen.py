"""
title: data_gen.py
original title: buildspace_clicktest_csv_agg
author: Clayton Bennett
created: 2 August 2024

Naming:

"""
import csv
import random
import math

def main():
    global util
    global self
    util = Utilities()
    gen = Generate()

    time_data = list(util.linspace(0,10,100))
    time_data = [round(x,2) for x in time_data]
    h = util.create_height_data()
    d = util.create_depth_data()
    vr = util.create_elliptical_vertical_radii_data()
    hr = util.create_elliptical_horiontal_radii_data()
    s = util.create_spin_data()
    c = util.create_color_data()

    data = [
            {"time":time_data},
            {"height":h},
            {"depth":d},
            {"vertical_radius":vr},
            {"horizontal_radius":hr},
            {"spin":s},
            {"color":c}
            ]
    print(data)
    if False:
        gen.export_each(filename_export,data)
    
    bool_success = gen.export_csv(h,d,vr,hr,s,c)
    
        #filename = "Buildspace_clicks.csv"
    filename = "space_delimited_clickdata.csv"

    def export_csv(time_data,
                   height_data,
                   depth_data,
                   vertical_radius_data,
                   horizontal_radius_data,
                   spin_sata,
                   color_data):
            
        with open(filename, mode ='r')as file:
            csvFile = csv.reader(file, delimiter = " ")
            for i,row in enumerate(csvFile):
                if i>0: 
                    name = row[0]   
                    day = row[1]
                    house = row[2]
                    value = int(eval(row[3])) # from spreasheet
                    filename_export = util.makename(name,house,day)
                    data = [
                            {"time":time_data},
                            {"height":height_data},
                            {"depth":depth_data},
                            {"vertical_radius":vertical_radius_data},
                            {"horizontal_radius":horizontal_radius_data},
                            {"spin":spin_sata},
                            {"color":color_data}
                            ]
                    gen.export_each(filename_export,data)

                
    # radii are not a subgroup. Each is independent of the other,
    # though meaning and narrative can be coupled if the user choses.
    
class Utilities:
    @staticmethod
    def linspace(start, stop, n):
        if n == 1:
            yield stop
            return
        h = (stop - start) / (n - 1)
        for i in range(n):
            yield start + h * i

class Data:
    @staticmethod
    def create_height_data(midline, time_data):
        # harmoni waves, polynomial
        height_data = []
        amp = midline/random.uniform(45,200)
        k = 1
        period = random.uniform(0.2,0.5)
        for x in time_data:
            y = round(amp*math.sin(period*x)+midline,0)
            height_data.append(y)
        return height_data

    @staticmethod
    def create_depth_data(time_data):
        depth_data = []
        for t in time_data:
            a = 1
            θ = t
            r = a + cosθ # cardioid
            #r2 = a - cosθ # cardioid
            depth_data.append(r)
            
    @staticmethod
    def create_color_data(time_data):
        color_data = []
        for t in time_data:
            c = None
            color_data.append(c)
        pass
    
    @staticmethod
    def create_elliptical_vertical_radii_data(time_data): 
        vertical_radius_data = []
        for t in time_data:
            vr = None
            vertical_radius_data.append(vr)
        pass
    
    @staticmethod
    def create_elliptical_horiontal_radii_data(time_data): 
        horizontal_radius_data = []
        for t in time_data:
            hr = None
            horizontal_radius_data.append(hr)
        pass
    
    @staticmethod
    def create_spin_data(time_data):
        spin_data = []
        for t in time_data:
            s = None
            spin_data.append(s)
        pass

class Generate:
    @staticmethod
    def makename(name,house,day):
        filename = name+"_"+house+"_"+day+"0.csv"
        return filename

    @staticmethod
    def export_each(filename,time_data,height_data):
        with open(filename, 'w', newline='') as csvfile:
            fieldnames = [".", "score"]
            writer = csv.writer(csvfile)
            writer.writerow(fieldnames)
            for i,r in enumerate(time_data):
                writer.writerow([time_data[i],height_data[i]])



if __name__ == '__main__':
    main()

