from commands2 import Subsystem
from constants import TurretConstant
import wpilib
import phoenix5
import phoenix6

from wpilib import SmartDashboard
class Turret(Subsystem):
    def __init__(self):
        super().__init__()

        self.rotate_motor = phoenix5.WPI_TalonSRX(TurretConstant.kRotateMotor)
        self.lift_motor = phoenix5.WPI_TalonSRX(TurretConstant.kLiftMotor)

        if False: # Install Rotate Motor Limit Switchs
            self.rotate_motor.configForwardLimitSwitchSource(phoenix5.LimitSwitchSource.FeedbackConnector, phoenix5.LimitSwitchNormal.NormallyOpen)
            self.rotate_motor.configReverseLimitSwitchSource(phoenix5.LimitSwitchSource.FeedbackConnector, phoenix5.LimitSwitchNormal.NormallyOpen) 
        
        if False: # Install Lift Motor Limit Switchs
            self.lift_motor.configForwardLimitSwitchSource(phoenix5.LimitSwitchSource.FeedbackConnector, phoenix5.LimitSwitchNormal.NormallyOpen)
            self.lift_motor.configReverseLimitSwitchSource(phoenix5.LimitSwitchSource.FeedbackConnector, phoenix5.LimitSwitchNormal.NormallyOpen)

        SmartDashboard.putData("Turret Rotate Motor", self.rotate_motor)
        SmartDashboard.putData("Turret Lift Motor", self.lift_motor)

    def move_rotate(self, speed: float):
        #make sure the turret is within the limits
        motor = self.rotate_motor
        forward_limit = motor.getSensorCollection().isFwdLimitSwitchClosed()
        reverse_limit = motor.getSensorCollection().isRevLimitSwitchClosed()

        motor.set(0 if forward_limit or reverse_limit else speed)

    def move_lift(self, speed: float):
        #make sure the turret is within the limits
        motor = self.lift_motor
        forward_limit = motor.getSensorCollection().isFwdLimitSwitchClosed()
        reverse_limit = motor.getSensorCollection().isRevLimitSwitchClosed()

        motor.set(0 if forward_limit or reverse_limit else speed)
    
    def aimWithJoystick(self, joystick: wpilib.Joystick):# rotate_speed: float, lift_speed: float):
        rotate_speed = joystick.getRightX() ** 3 #try to allow for fine control
        lift_speed = joystick.getRightY() ** 3 #try to allow for fine control
        
        self.move_rotate(rotate_speed)
        self.move_lift(lift_speed)

    def stop_rotate(self):
        self.rotate_motor.set(0)

    def stop_lift(self):
        self.lift_motor.set(0)

    def periodic(self):
        pass
