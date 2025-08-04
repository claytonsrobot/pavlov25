'''
Author: Clayton Bennett
Created: 05 November 2023
Title: text_pyplot.py

Purpose: Input all points for entire character, copy paste. Or, import whole file.
Lay ground work for plotting in FBX. However, for now, use for development and visualization.

Create all glyphs for:
glyphs = list(map(chr, range(40,96)))
alphabet = list(string.ascii_uppercase)

07 November 2023:
All letters and numbers finished.
To do: '[', '\\', ']', '^', '_','(', ')', '*', '+', ',', '-', '.', '/',':', ';', '<', '=', '>', '?', '@'
Maybe just do: '[', '\', ']', '^', '_','(', ')', '*', '+', ',', '-', '.', '/',':','<','>'

If there is character internl/external loop overlap if should be externally CCW
'''

import matplotlib.pyplot as plt
import numpy as np
import os
import math
    
characters = ['char64']
#characters = ['(',')','I','L']
filenames = []
for character in characters:
    filename = character+'_svg.html'
    filenames.append(filename)


directory = r"..\alphanumeric_character_library" 
directory = os.path.normpath(directory)

fig = plt.figure()

plotx,ploty=1,1
for filename in filenames:

    #plt.subplot(len(filenames),ploty,plotx)
    ax = fig.add_subplot(2,math.ceil(len(filenames)/2),plotx)
    #ax = fig.add_subplot(2,3,plotx)
    #ax = fig.add_subplot(1,len(filenames),plotx)
    #ax.figsize(8,5)
    html_file = open(directory+'\\'+filename,'r', encoding = 'utf-8')
    raw = html_file.read()
    # find instances of <line and <polyline
    # when you find these, find go right/down until you find the next >

    # when you find one instance of <line or <polyline, then find the next instance of >. After this, spit out the remaining string to the right, to search again, until no instance are left.
    polyline_chunks = []
    line_chunks = []
    remainder = raw


    major_ticks = np.arange(0,101,5)
    minor_ticks = np.arange(0,101,5)
    ax.set_xticks(major_ticks)
    ax.set_xticks(minor_ticks,minor=True)
    ax.set_yticks(major_ticks)
    ax.set_yticks(minor_ticks,minor=True)
    plt.xticks(rotation=90)
    ax.set_aspect('equal')
    ax.grid(which='both')
    ax.invert_yaxis()
    '''
    # find each instance of '<line' to '>' then remove from remainder, add to chunks
    # find each instance of '<polyline' to '>' then remove from remainder, add to chunks
    line_start_idx = remainder.find('<line')
    if line_start_idx!=-1:
        line_end_idx = remainder[line_next_idx:].find('>')
        line_chunk = [line_next_idx,line_end_idx]
        remainder.pop(line_chunk)

        
    polyline_next_idx = remainder.find('<polyline')
    start_idx = [line_next_idx,polyline_next_idx]
    for i,item in enumerate(start_idx):
        if item==-1:
            start_idx.pop(i)
    start_idx = start_idx[0]


    '''
    remainder = raw

    polylines = []
    #polyline_chunks = []
    while '<polyline' in remainder:
        start_str = '<polyline'
        stop_str = 'style'
        start_idx = remainder.find(start_str)
        stop_idx = remainder.find(stop_str,start_idx+len(start_str))
        chunk = remainder[start_idx:stop_idx]

        start_str_data = 'points = "'
        start_idx_data = chunk.find(start_str_data)+len(start_str_data) 
        stop_idx_data = chunk.find('"',start_idx_data+len(start_str_data))
        chunk = chunk[start_idx_data:stop_idx_data]

        #polyline_chunks.append(chunk)
        polyline = np.array(chunk.replace(' ',',').split(','),dtype=float).reshape(-1,2)
        x = polyline[:, 0]
        y = polyline[:, 1]
        plt.plot(x,y)
        polylines.append(polyline)
        
        remainder = remainder[0:start_idx]+remainder[stop_idx+1:]
    #polylines = np.array(polylines)

        
        

    #line_chunks = []
    lines = []
    remainder = raw
    while '<line' in remainder:
        start_str = '<line'
        stop_str = 'style'
        start_idx = remainder.find(start_str)
        stop_idx = remainder.find(stop_str,start_idx+len(start_str))
        chunk = remainder[start_idx:stop_idx]

        values = []
        remainder_chunk = chunk
        while '=' in remainder_chunk:
            start_str_data = '="'
            stop_str_data = '"'
            start_idx_data = remainder_chunk.find(start_str_data)+len(start_str_data)
            #stop_idx_data = remainder_chunk.find(stop_str_data,start_idx_data+len(start_str_data))
            stop_idx_data = remainder_chunk.find(stop_str_data,start_idx_data+1)
            value = remainder_chunk[start_idx_data:stop_idx_data]
            #print("value = ",value)
            value = float(value)
            remainder_chunk = remainder_chunk[stop_idx_data:]
            
            values.append(value)
        line = np.array(values).reshape(-1,2)
        [[x1,y1],[x2,y2]]=line
        plt.plot([x1,x2],[y1,y2])
        
        lines.append(line)
        
        #line_chunks.append(chunk)
        remainder = remainder[0:start_idx]+remainder[stop_idx+1:]
    lines = np.array(lines)
    plotx=plotx+1



plt.show()
