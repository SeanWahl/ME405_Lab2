from time import ticks_us, ticks_add, ticks_diff
from motor_driver import MotorDriver
from encoder_reader import encoder
from controller import CLController

S0_INIT           = 0
S1_INPUT_SETPOINT = 1
S2_INPUT_KP       = 2
S3_RUN            = 3
S4_PRINT          = 4

state = S0_INIT

times = []
thetas = []

if __name__ == "__main__":
    while True:#do stuff
        if state == S0_INIT:
            my_motor = MotorDriver(pyb.Pin.board.PA10, pyb.Pin.board.PB4, pyb.Pin.board.PB5, 3)
            my_encoder = encoder(pyb.Pin.board.PC6, pyb.Pin.board.PC7, 8)
            my_controller = CLController(.2, 256*4*16)
            u2 = pyb.UART(2, baudrate=115200)
            state = S1_INPUT_SETPOINT
            
        if state == S1_INPUT_SETPOINT:
            my_setpoint = input('Please input a setpoint: ')
            try:
                my_controller.set_Setpoint(float(my_setpoint))
            except:
                print('Input a valid setpoint!')
            else:
                state = S2_INPUT_KP
                
        if state == S2_INPUT_KP:
            my_Kp = input('Please input a gain (Kp): ')
            try:
                my_controller.set_Kp(float(my_Kp))
            except:
                print('Input a valid gain!')
            else:
                state = S3_RUN
                my_encoder.zero()
                t_init = ticks_us()
                t_last = t_init
                
        if state == S3_RUN:
            t_current = ticks_us()
            if ticks_diff(t_current, t_last) >= 10_000:
                theta = my_encoder.read_encoder()
                my_motor.set_duty_cycle(my_controller.run(theta))
                times.append(ticks_diff(t_current, t_init)/1_000)
                thetas.append(theta)
                t_last = t_current
            if ticks_diff(ticks_us(), t_init) >= 5_000_000:
               my_motor.set_duty_cycle(0)
               state = S4_PRINT
               
        if state == S4_PRINT:
            for idx in range(len(times)):
                u2.write(f"{times[idx]}, {thetas[idx]}\r\n")
            u2.write('done\r\n')
            print('done')
            times = []
            thetas = []
            state = S1_INPUT_SETPOINT
