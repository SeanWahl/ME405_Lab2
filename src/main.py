"""!@file main.py
@brief      Runs a motor step response based on user inputs.
@details    When run, this file asks the user for a setpoint and a proportional
            gain (K_p) value to do perform a motor step response with. The controller
            runs every 10ms and at each step the time and the encoder reading is
            recorded. After running, these values shall be transmitted through a 
            serial port for plotting. See computerPlotting.py for details.
            Lastly, the program resets and asks for new step response parameters.
@author     Nathan Dodd
@author     Lewis Kanagy
@author     Sean Wahl
@date       February 7, 2023
"""

# Import necessary modules to run this file
import pyb
from time import ticks_us, ticks_diff
from motor_driver import MotorDriver
from encoder_reader import encoder
from controller import CLController

## An initializing state in which the motor, encoder, controller, and serial port are set up.
S0_INIT           = 0
## A user input state in which a controller setpoint is taken.
S1_INPUT_SETPOINT = 1
## A user input state in which a proportional gain value is taken.
S2_INPUT_KP       = 2
## A state which runs the step response on the motor.
S3_RUN            = 3
## A state in which the data recorded in the run state is transmitted through a UART to a 
#  secondary virtual COM port for plotting purposes.
S4_PRINT          = 4

## The state the program is currently running in.
state = S0_INIT

## A list of time data taken during the step response.
times = []
## A list of encoder readings (in ticks) taken during the step response.
thetas = []

if __name__ == "__main__":
    while True:
        
        if state == S0_INIT:
            # Intialize the necessary hardware/software objects for this file.
            
            ## A motor object to control duty cycles.
            my_motor = MotorDriver(pyb.Pin.board.PA10, pyb.Pin.board.PB4, pyb.Pin.board.PB5, 3)
            ## An encoder object to measure the motor's shaft position (in ticks)
            my_encoder = encoder(pyb.Pin.board.PC6, pyb.Pin.board.PC7, 8)
            ## A controller object to perfrom closed loop control on the motor using the encoder.
            my_controller = CLController(.2, 256*4*16)
            ## A UART object for transmitting data through the serial port.
            u2 = pyb.UART(2, baudrate=115200)
            state = S1_INPUT_SETPOINT
            
        if state == S1_INPUT_SETPOINT:
            # Take a user input setpoint.
            
            ## A user input setpoint for the controller.
            my_setpoint = input('Please input a setpoint: ')
            try:
                my_controller.set_Setpoint(float(my_setpoint))
            except:
                print('Input a valid setpoint!')
            else:
                state = S2_INPUT_KP
                
        if state == S2_INPUT_KP:
            # Take a user input proportional gain value.
            
            ## A user input proportional gain for the controller.
            my_Kp = input('Please input a gain (Kp): ')
            try:
                my_controller.set_Kp(float(my_Kp))
            except:
                print('Input a valid gain!')
            else:
                state = S3_RUN
                my_encoder.zero()
                ## The time at which the step response starts.
                t_init = ticks_us()
                ## The time at which the controller was last run.
                t_last = t_init
                
        if state == S3_RUN:
            # Run the step response by calling the controller every 10ms.
            
            ## The current time at which the controller is running.
            t_current = ticks_us()
            if ticks_diff(t_current, t_last) >= 10_000:
                ## The current encoder reading in ticks.
                theta = my_encoder.read_encoder()
                my_motor.set_duty_cycle(my_controller.run(theta))
                times.append(ticks_diff(t_current, t_init)/1_000)
                thetas.append(theta)
                t_last = t_current
            if ticks_diff(ticks_us(), t_init) >= 5_000_000:
               my_motor.set_duty_cycle(0)
               state = S4_PRINT
               
        if state == S4_PRINT:
            # Send the recorded times and thetas through the serial port secondary receival.
            
            for idx in range(len(times)):
                u2.write(f"{times[idx]}, {thetas[idx]}\r\n")
            u2.write('done\r\n')
            print('done')
            
            # Reset the data lists.
            times = []
            thetas = []
            state = S1_INPUT_SETPOINT
