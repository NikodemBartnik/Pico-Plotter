# Pico Plotter
![Pico Plotter image](../Docs/Images/mini.JPG)
3D printed Raspberry Pi Pico H-Bot plotter programmed in MicroPython capable of drawing on paper and burning wood with versatip.

## Description

Main purpose of this project was to practice Python programing, design something cool and understand basics of how CNC machines, Gcode senders etc. works. This project is probably a great starting point to learn about basics of any CNC machine, as it is very simple and code is very minimal. 3D printed parts are optimized for support less printing (most of them but not all) and can be printed out of PLA. 

## Getting Started
You don't need any special libraries or additional files, assuming you have Python installed you have everything you need.
In order to upload script to Raspberry Pi Pico I used [Thonny](https://thonny.org/)

### Executing program
Before executing the Gcode sender change port of your raspberry pi pico and also path to the file that you want to print
To execute Gcode sender script simply change directory to where the file is located and type in the terminal:
```
python GcodeSender.py
```

## Help

If you need help, see the problem or want to contribute open an issue.

## Author
[Nikodem Bartnik](https://nikodembartnik.pl/)


## License

This project is licensed under the MIT license.