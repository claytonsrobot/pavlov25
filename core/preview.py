'''
Author: Clayton Bennett
Created: 12 March 2024
Title: preview.py

show scene without yet generating and FBX export
'''
import os
import numpy as np
            

if True:
    #import matplotlib # hungry hungry hippo
    import matplotlib.pyplot as plt

class Preview:
    scene_object=None
    style_object=None
    user_input_object=None

    @classmethod
    def assign_scene_object_etc(cls, scene_object):
        cls.style_object = scene_object.style_object
        cls.scene_object = scene_object
        cls.user_input_object = scene_object.user_input_object

    def __init__(self):
        self.name = os.path.basename(__file__).removesuffix('.py')

    def build(self,scene_object):
        print('develop_preview')
        print(f"bokeh:{bokeh}")
        scene_object
    
    def show(self):
        print('develop_preview')
        pp=plt
        pp.show()
    def sample(self):
        #https://jakevdp.github.io/PythonDataScienceHandbook/04.12-three-dimensional-plotting.html
        

        from mpl_toolkits import mplot3d


        #%matplotlib inline
        

        fig = plt.figure()
        ax = plt.axes(projection='3d')

        # Data for a three-dimensional line
        zline = np.linspace(0, 15, 1000)
        xline = np.sin(zline)
        yline = np.cos(zline)
        ax.plot3D(xline, yline, zline, 'gray')

        # Data for three-dimensional scattered points
        zdata = 15 * np.random.random(100)
        xdata = np.sin(zdata) + 0.1 * np.random.randn(100)
        ydata = np.cos(zdata) + 0.1 * np.random.randn(100)
        ax.scatter3D(xdata, ydata, zdata, c=zdata, cmap='Greens')
        if False:
            ax.set_axis_off()

        #fig.set_facecolor('black')
        #ax.set_facecolor('black') 
        #ax.grid(False) 
        #ax.w_xaxis.pane.fill = False
        #ax.w_yaxis.pane.fill = False
        #ax.w_zaxis.pane.fill = False
        #ax.w_xaxis.set_pane_color((0.0, 0.0, 0.0, 0.0))
        #ax.w_yaxis.set_pane_color((0.0, 0.0, 0.0, 0.0))
        #ax.w_zaxis.set_pane_color((0.0, 0.0, 0.0, 0.0))

        fig.show()

    def curve_make(self,curve_object):
        time = curve_object.time+curve_object.data_origin_relative_to_scene_data_origin[0]
        height = curve_object.height+curve_object.data_origin_relative_to_scene_data_origin[1]
        depth = curve_object.depth+curve_object.data_origin_relative_to_scene_data_origin[2]
        
        #curve_object.time,curve_object.height,curve_object.depth
        return time,height,depth

    def label_placement(self,curve_object):
        x=curve_object.title_object.element_minimum_corner_origin_relative_to_curve_data_origin[0]+curve_object.data_origin_relative_to_scene_data_origin[0]
        y=curve_object.title_object.element_minimum_corner_origin_relative_to_curve_data_origin[1]+curve_object.data_origin_relative_to_scene_data_origin[1]
        z=curve_object.title_object.element_minimum_corner_origin_relative_to_curve_data_origin[2]+curve_object.data_origin_relative_to_scene_data_origin[2]
        return x,y,z
        
    def preview_scene3D(self,scene_object):
        from mpl_toolkits import mplot3d
        #%matplotlib inline
        
        fig = plt.figure()
        ax = plt.axes(projection='3d')
        #ax2 = plt.axes(projection='3d')
        
        for curve_object in self.scene_object.hierarchy_object.dict_curve_objects_all.values():
            #if curve_object.supergroup.supergroup.name == 'Alturus':
            time,height,depth = self.curve_make(curve_object)
            ax.plot3D(time,height,depth)
            #ax.plot3D(time,height,depth,'gray')
            #ax.scatter3D(time,height,depth)

            x,y,z=self.label_placement(curve_object)
            label = curve_object.name
            #ax.text(x, y, z, label, 'x',color = 'white')
            ax.text(x, y, z, label, 'x',color = 'black')

        '''for curve_object in hierarchy_object.dict_curve_objects_all.values():
            if curve_object.supergroup.supergroup.name == 'Seahawk':
                time,height,depth = self.curve_make(curve_object)
                ax2.plot3D(time,height,depth)
                #ax.plot3D(time,height,depth,'gray')
                #ax.scatter3D(time,height,depth)

                x,y,z=self.label_placement(curve_object)
                label = curve_object.name
                #ax.text(x, y, z, label, 'x',color = 'white')
                ax2.text(x, y, z, label, 'x',color = 'black')'''
                
                
        #ax.text(x, y, z, label, 'x')
        #ax.text(x, y, z, 'dave',color = 'white')
        #ax.text(0, 0, 0, 'dave',color = 'white')
        
        # matplotlib.rcParams.update({'font.size': 8})

        
        if False:
            ax.set_axis_off()

        #fig.set_facecolor('black')
        #ax.set_facecolor('black')

        '''ax.xaxis.label.set_color('red')        #setting up X-axis label color to yellow
        ax.yaxis.label.set_color('red')          #setting up Y-axis label color to blue

        ax.tick_params(axis='x', colors='red')    #setting up X-axis tick color to red
        ax.tick_params(axis='y', colors='red')  #setting up Y-axis tick color to black

        ax.spines['left'].set_color('red')        # setting up Y-axis tick color to red
        ax.spines['top'].set_color('red')         #setting up above X-axis tick color to red'''

        # if matplot lib is used, stack should be depth-depth-depth, so that the time axis is relevant
        # or maybe we can have multiple plots

        ##https://www.originlab.com/doc/Tutorials/3D-Stack-Surface
        
        #ax.grid(False) 
        #ax.w_xaxis.pane.fill = False
        #ax.w_yaxis.pane.fill = False
        #ax.w_zaxis.pane.fill = False
        #ax.w_xaxis.set_pane_color((0.0, 0.0, 0.0, 0.0))
        #ax.w_yaxis.set_pane_color((0.0, 0.0, 0.0, 0.0))
        #ax.w_zaxis.set_pane_color((0.0, 0.0, 0.0, 0.0))

        fig.show()

if __name__ == "__main__":
    preview_object = Preview()
    #preview_object.assign_scene_object_etc(scene_object)
    #preview_object.build()
    #preview_object.show()
    preview_object.sample()
        





