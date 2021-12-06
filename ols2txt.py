# -*- coding: utf-8 -*-
"""
Created on Fri Nov 26 11:24:21 2021

@author: joao.levandoski
"""

import os
import numpy as np

from tkinter import filedialog as fd
from tkinter import Tk


def open_ols(file_path):
    with open(file_path, "rb") as f:
        if not f.readline() == b'<Olis dataset version 1.0>\r\n':
            raise ValueError('Not a correct OLS file, wrong header.')


        i = 0
        next_line = False
        points_x = False
        points_y = False
        line_start = False 
        line_step = False
        second_start = False
        second_step = False
        axis_z = False
        while True:
            i += 1
            if i> 1000:
                break

            l = f.readline().decode('latin_1')
            
            if points_x:
                n_points_x = int(str(l).strip())
                points_x = False
            elif points_y:
                n_points_y = int(str(l).strip())
                points_y = False
            elif line_start:
                start = float(str(l).strip())
                line_start = False
            elif line_step:
                step = float(str(l).strip())
                line_step = False

            if '<BinData>' in str(l) and axis_z:
                break
            elif '<Number of Points>' in str(l) and not next_line:
                next_line = True
                points_x = True
            elif '<Number of Points>' in str(l) and next_line:
                points_y = True
            elif '<Start>' in str(l) and not second_start:
                line_start = True
                second_start = True
            elif '<Step>' in str(l) and not second_step:
                line_step = True
                second_step = True
            elif '<ZAxis>' in str(l):
                axis_z = True


        f.seek(0, 1)

        X = np.fromfile(f, dtype='float64', count=n_points_x*n_points_y).reshape(n_points_x, n_points_y)

    stop = start + n_points_x*step
    wavelenght = np.arange(start, stop, step)
    
    return wavelenght, X

if __name__ == "__main__":

    root = Tk()
    root.withdraw()
    folder = fd.askdirectory(title="Select folder with all *.ols files")
    files = os.listdir(folder)
    
    
    root = Tk()
    root.withdraw()
    folder_save = fd.askdirectory(title="Select to save *.txt files")
    
    print(folder)
    j = 0
    for name in files:
        if name.split('.')[-1] == 'ols':
            try:
                path_file = str(folder) + '/' + str(name)
                path_save = str(folder_save) + '/' + str(name).replace('.ols', '')
    
                print(path_file.split('/')[-1], '-- CONVERTING . . . ')
                
                wave, x = open_ols(path_file)
                
                wave1 = wave.reshape(len(wave), 1)
                
                for i in range(x.shape[-1]):
                    full_file = np.concatenate((wave1[::-1], x[::, i][::-1].reshape(len(wave), 1)), axis=1)    
                        
                    np.savetxt(f'{path_save}_converted_{i+1}.txt', 
                               full_file, 
                               fmt='%.9f', 
                               delimiter=' ', 
                               newline='\n', 
                               header='', 
                               footer='', 
                               comments='# ', 
                               encoding=None)
                print(path_file.split('/')[-1],' DONE')
                print()
                j += 1
            except:
                print(path_file.split('/')[-1],' Fail')
    
    print(f'{j} Files was converted')