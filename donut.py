#!/usr/bin/env python3
import time
import os
import math
import sys

def clear_screen():
    
    os.system('cls' if os.name == 'nt' else 'clear')

def get_color_code(value):
    
    colors = [
        '\033[38;5;21m',   # Синий
        '\033[38;5;27m',   # Светло-синий
        '\033[38;5;39m',   # Голубой
        '\033[38;5;51m',   # Бирюзовый
        '\033[38;5;46m',   # Зеленый
        '\033[38;5;82m',   # Салатовый
        '\033[38;5;226m',  # Желтый
        '\033[38;5;214m',  # Оранжевый
        '\033[38;5;196m',  # Красный
        '\033[38;5;201m',  # Розовый
        '\033[38;5;129m',  # Фиолетовый
        '\033[38;5;93m',   # Пурпурный
    ]
    
    
    idx = int(value * (len(colors) - 1)) % len(colors)
    return colors[idx]

def spinning_colorful_donut():
    
    try:
        clear_screen()
        print("\033[2J\033[H", end='')  
        
        A = 0.0  # Угол вращения A
        B = 0.0  # Угол вращения B
        
        
        width = 80
        height = 24
        
        reset_color = '\033[0m'
        
        frame = 0
        
        while True:
            
            z = [0.0] * (width * height)
            b = [' '] * (width * height)
            
            
            theta = 0.0
            while theta < 2 * math.pi:
                
                phi = 0.0
                while phi < 2 * math.pi:
                   
                    costheta = math.cos(theta)
                    sintheta = math.sin(theta)
                    cosphi = math.cos(phi)
                    sinphi = math.sin(phi)
                    
                    
                    cosA = math.cos(A)
                    sinA = math.sin(A)
                    cosB = math.cos(B)
                    sinB = math.sin(B)
                    
                    
                    circle_x = 2 + costheta
                    x = circle_x * (cosB * cosphi + sinA * sinB * sinphi) - sintheta * cosA * sinB
                    y = circle_x * (sinB * cosphi - sinA * cosB * sinphi) + sintheta * cosA * cosB
                    z_coord = cosA * circle_x * sinphi + sintheta * sinA
                    
                    
                    ooz = 1 / (z_coord + 5)  
                    
                   
                    xp = int(width / 2 + 30 * ooz * x)
                    yp = int(height / 2 - 15 * ooz * y)
                    
                   
                    luminance = cosphi * costheta * sinB - cosA * costheta * sinphi - sinA * sintheta + cosB * (cosA * sintheta - costheta * sinA * sinphi)
                    
                   
                    idx = xp + width * yp
                    
                    if 0 <= yp < height and 0 <= xp < width and ooz > z[idx]:
                        z[idx] = ooz
                        
                        
                        if luminance > 0:
                            lum_idx = int(luminance * 8)
                            if lum_idx > 11:
                                lum_idx = 11
                            chars = ".,-~:;=!*#$@%&"
                            b[idx] = chars[lum_idx % len(chars)]
                        else:
                            b[idx] = '.'
                    
                    phi += 0.02
                theta += 0.02
            
           
            sys.stdout.write('\033[H')
            
           
            for i in range(height):
                for j in range(width):
                    idx = i * width + j
                    char = b[idx]
                    if char != ' ':
                       
                        brightness = min(1.0, z[idx] * 2)
                        color = get_color_code(brightness * 10 + frame * 0.1)
                        sys.stdout.write(color + char + reset_color)
                    else:
                        sys.stdout.write(' ')
                sys.stdout.write('\n')
            
       
            A += 0.04
            B += 0.02
            frame += 1
            
           
            time.sleep(0.03)
            
    except KeyboardInterrupt:
        clear_screen()
        print("\033[{}mСпасибо за просмотр! Пончик остановлен.{}\033[0m".format(
            '\033[93m', '\033[0m'
        ))

def spinning_colorful_donut_enhanced():
  
    try:
        clear_screen()
        print("\033[2J\033[H", end='')
        
        A = 0.0
        B = 0.0
        
        width = 80
        height = 24
        
        reset_color = '\033[0m'
        
       
        colors = [f'\033[38;5;{i}m' for i in range(16, 232)]
        
        frame = 0
        
        while True:
            z = [0.0] * (width * height)
            b = [' '] * (width * height)
            
           
            for theta in range(0, 628, 6):  
                for phi in range(0, 628, 3):  
                 
                    t = theta / 100.0
                    p = phi / 100.0
                    
                   
                    cost = math.cos(t)
                    sint = math.sin(t)
                    cosp = math.cos(p)
                    sinp = math.sin(p)
                    
                    
                    cosA = math.cos(A)
                    sinA = math.sin(A)
                    cosB = math.cos(B)
                    sinB = math.sin(B)
                    
                
                    circlex = 2 + cost
                    x = circlex * (cosB * cosp + sinA * sinB * sinp) - sint * cosA * sinB
                    y = circlex * (sinB * cosp - sinA * cosB * sinp) + sint * cosA * cosB
                    zcoord = cosA * circlex * sinp + sint * sinA
                    
                  
                    ooz = 1 / (zcoord + 5)
                    
                    xp = int(width / 2 + 30 * ooz * x)
                    yp = int(height / 2 - 15 * ooz * y)
                    
                    
                    luminance = cosp * cost * sinB - cosA * cost * sinp - sinA * sint + cosB * (cosA * sint - cost * sinA * sinp)
                    
                    idx = xp + width * yp
                    
                    if 0 <= yp < height and 0 <= xp < width and ooz > z[idx]:
                        z[idx] = ooz
                        
                       
                        if luminance > 0:
                           
                            chars = ".,-~:;=!*#$@%&"
                            char_idx = min(int(luminance * 12), len(chars) - 1)
                            b[idx] = chars[char_idx]
                            
                          
                            color_idx = int((xp * 0.5 + yp * 0.3 + frame * 2) % len(colors))
                            sys.stdout.write(colors[color_idx] + b[idx] + reset_color)
                        else:
                            b[idx] = '.'
                            sys.stdout.write('\033[38;5;240m.\033[0m')  
            
           
            sys.stdout.write('\033[H')
            output = []
            for i in range(height):
                for j in range(width):
                    idx = i * width + j
                    char = b[idx]
                    if char != ' ':
                        if char != '.':
                        
                            color_idx = int((j * 0.5 + i * 0.3 + frame * 2) % len(colors))
                            output.append(colors[color_idx] + char + reset_color)
                        else:
                            output.append('\033[38;5;240m.\033[0m')
                    else:
                        output.append(' ')
                output.append('\n')
            
            sys.stdout.write(''.join(output))
            
           
            A += 0.05
            B += 0.03
            frame += 1
            
            time.sleep(0.03)
            
    except KeyboardInterrupt:
        clear_screen()
        rainbow_text = ""
        for i, char in enumerate("До свидания! Спасибо за просмотр!"):
            color = f'\033[38;5;{16 + (i * 10) % 216}m'
            rainbow_text += color + char
        print(rainbow_text + '\033[0m')

def main():

    clear_screen()
    
 
    title = """PONCHUCK"""
    
    print("\033[38;5;201m" + title + "\033[0m")
    print("\n\033[38;5;46mВыберите версию:\033[0m")
    print("\033[38;5;39m1. \033[38;5;226mКлассический цветной пончик\033[0m")
    print("\033[38;5;39m2. \033[38;5;214mУлучшенный пончик с градиентом\033[0m")
    print("\033[38;5;39m3. \033[38;5;196mВыход\033[0m")
    
    choice = input("\n\033[38;5;46mВаш выбор (1-3): \033[0m")
    
    if choice == '1':
        print("\n\033[38;5;226mЗапуск классического пончика... (нажмите Ctrl+C для остановки)\033[0m")
        time.sleep(2)
        spinning_colorful_donut()
    elif choice == '2':
        print("\n\033[38;5;214mЗапуск улучшенного пончика... (нажмите Ctrl+C для остановки)\033[0m")
        time.sleep(2)
        spinning_colorful_donut_enhanced()
    else:
        clear_screen()
        print("\033[38;5;196mДо свидания!\033[0m")

if __name__ == "__main__":
    main()
