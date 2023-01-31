from motor_driver import MotorDriver
from encoder_reader import encoder
import utime

class CLController:
    
    def __init__(self, Kp, Setpoint):
        """!@brief             adsf
            @details           asdfa
            @param   Kp        asdf
            @param   Setpoint  asdf
        """   
        self.Kp = Kp
        self.Setpoint = Setpoint
    
    def run(self, Actual):
        """!@brief		    asdf
            @param  Actual  asdf
        """
        Actuation = self.Kp * (self.Setpoint - Actual)
        return Actuation
    
    def set_Kp(self, Kp):
        """!@brief		asdf
            @param  Kp  asdf
        """
        self.Kp = Kp
    
    def set_Setpoint(self, Setpoint):
        """!@brief		      asdf
            @param  Setpoint  asdf
        """
        self.Setpoint = Setpoint
        
if __name__ == "__main__":
    my_motor = MotorDriver(pyb.Pin.board.PA10, pyb.Pin.board.PB4, pyb.Pin.board.PB5, 3)
    my_encoder = encoder(pyb.Pin.board.PC6, pyb.Pin.board.PC7, 8)
    my_controller = CLController(.2, 100000)
    my_encoder.zero()
    print(my_encoder.read_encoder())
    for idx in range(500):
        my_motor.set_duty_cycle(my_controller.run(my_encoder.read_encoder()))
        utime.sleep_ms(10)
    print('done')
    print(my_encoder.read_encoder())
    my_motor.set_duty_cycle(0)