from wpilib import SmartDashboard
from wpimath.geometry import Rotation2d
import wpilib
import wpilib.drive

import commands2
import phoenix5
import math

from constants import DriveConstant

class DriveTrain(commands2.Subsystem):
    def __init__(self) -> None:
        """Creates a new DriveSubsystem"""
        super().__init__()
        # Register the subsystem with the CommandScheduler
        # CommandScheduler.getInstance().registerSubsystem(self) when calling it in robot it registers it

        self.right_invert_YN = True
        
        # We need to invert one side of the drivetrain so that positive voltages
        # result in both sides moving forward. Depending on how the robot's
        # gearbox is constructed, you might have to invert the left side instead.
        self.frontLeftMotor = phoenix5.WPI_TalonSRX(DriveConstant.kLeftMotor1Port)
        self.frontRightMotor = phoenix5.WPI_TalonSRX(DriveConstant.kRightMotor1Port)
        self.backLeftMotor = phoenix5.WPI_TalonSRX(DriveConstant.kLeftMotor2Port)
        self.backRightMotor = phoenix5.WPI_TalonSRX(DriveConstant.kRightMotor2Port)
        # self.frontRightMotor.getSimCollection().getMotorOutputLeadVoltage()

        SmartDashboard.putData("frontLeftMotor -from drivetrain", self.frontLeftMotor)
        SmartDashboard.putData("frontRightMotor -from drivetrain", self.frontRightMotor)
        SmartDashboard.putData("backLeftMotor -from drivetrain", self.backLeftMotor)
        SmartDashboard.putData("backRightMotor -from drivetrain", self.backRightMotor)

        if DriveConstant.kDriveType == "Tank":
            self.frontLeftMotor.setInverted(self.right_invert_YN)
            self.backLeftMotor.setInverted(self.right_invert_YN)
        else:
            self.frontRightMotor.setInverted(self.right_invert_YN)
            self.backRightMotor.setInverted(self.right_invert_YN)

        """ not using encoder yet
        # Set up encoders for each motor
        self.frontLeftEncoder = self.frontLeftMotor.getSensorCollection().getQuadraturePosition
        SmartDashboard.putNumber("frontLeftEncoder -from drivetrain", self.frontLeftEncoder())
        self.frontRightEncoder = self.frontRightMotor.getSensorCollection().getQuadraturePosition
        self.backLeftEncoder = self.backLeftMotor.getSensorCollection().getQuadraturePosition
        self.backRightEncoder = self.backRightMotor.getSensorCollection().getQuadraturePosition

        # Reset encoders to zero
        self.frontLeftMotor.getSensorCollection().setQuadraturePosition(0, 10)
        self.frontRightMotor.getSensorCollection().setQuadraturePosition(0, 10)
        self.backLeftMotor.getSensorCollection().setQuadraturePosition(0, 10)
        self.backRightMotor.getSensorCollection().setQuadraturePosition(0, 10)
        """
        match DriveConstant.kDriveType:
            case "Xdrive":
                self.robotDrive = TheWB_Xdrive(
                    self.frontLeftMotor,
                    self.frontRightMotor,
                    self.backLeftMotor,
                    self.backRightMotor,
                )
            case "Tank":
                self.backLeftMotor.follow(self.frontLeftMotor)
                self.backRightMotor.follow(self.frontRightMotor)
                self.robotDrive = wpilib.drive.DifferentialDrive(
                    self.frontLeftMotor, self.frontRightMotor
                )
            case "Mecanum":
                self.robotDrive = wpilib.drive.MecanumDrive(
                    frontLeftMotor=self.frontLeftMotor,
                    frontRightMotor=self.frontRightMotor,
                    rearLeftMotor=self.backLeftMotor,
                    rearRightMotor=self.backRightMotor,
                )

        # if DriveConstant.kIsMecanum:
        #     self.robotDrive = wpilib.drive.MecanumDrive(frontLeftMotor= self.frontLeftMotor,
        #                                                 frontRightMotor=self.frontRightMotor,
        #                                                 rearLeftMotor=self.backLeftMotor,
        #                                                 rearRightMotor=self.backRightMotor)
        # else:
        #     self.backLeftMotor.follow(self.frontLeftMotor)
        #     self.backRightMotor.follow(self.frontRightMotor)
        #     self.robotDrive = wpilib.drive.DifferentialDrive(self.frontLeftMotor, self.frontRightMotor)

        self.robotDrive.setMaxOutput(0.45)
        self.robotDrive.setDeadband(0.3)
        if DriveConstant.kDriveType != "Tank":
            self.robotDrive.driveCartesian(0, 0, 0)

        """rest are defaults so far:
        self.robotDrive.setExpiration(.05)"""

    def periodic(self) -> None:
        """This method will be called once per scheduler run"""
        # Add code here that needs to run periodically
        # SmartDashboard.putNumber("frontLeftMotor -from drivetrain getmotoroutputpercent", self.frontLeftMotor.getMotorOutputPercent())
        # SmartDashboard.putNumber("frontRightMotor -from drivetrain getmotoroutputpercent", self.frontRightMotor.getMotorOutputPercent())
        # SmartDashboard.putNumber("backLeftMotor -from drivetrain getmotoroutputpercent", self.backLeftMotor.getMotorOutputPercent())
        # SmartDashboard.putNumber("backRightMotor -from drivetrain getmotoroutputpercent", self.backRightMotor.getMotorOutputPercent())

        # SmartDashboard.putData("robotDrive -from drivetrain periodic", self.robotDrive)

    def driveWithJoystick(self, joystick: wpilib.Joystick):
        """Drives the robot using the joystick"""
        if isinstance(self.robotDrive, wpilib.drive.MecanumDrive):
            self.robotDrive.driveCartesian(
                joystick.getLeftX(),
                joystick.getRightX(),
                -joystick.getLeftY(),
                Rotation2d(0),
            )
        elif isinstance(self.robotDrive, wpilib.drive.DifferentialDrive):
            self.robotDrive.arcadeDrive(
                -joystick.getLeftY(), -((joystick.getRightX()) ** 5)
            )
        else:
            self.robotDrive.driveCartesian(
                -joystick.getLeftY(), -joystick.getLeftX(), joystick.getRightX()
            )

    def halt(self) -> None:
        self.robotDrive.driveCartesian(0, 0, 0)  # , Rotation2d(0))

    def slowLeft(self, joystick: wpilib.Joystick) -> None:
        self.robotDrive.driveCartesian(0, 0, -0.22, Rotation2d(0))

    def slowRight(self, joystick: wpilib.Joystick) -> None:
        self.robotDrive.driveCartesian(0, 0, 0.22, Rotation2d(0))

    # flight Checklist commands

    def OnlyFrontLeft(self) -> None:
        self.frontLeftMotor.set(0.51)

    def OnlyFrontRight(self) -> None:
        self.frontRightMotor.set(0.52)

    def OnlyBackLeft(self) -> None:
        self.backLeftMotor.set(0.53)

    def OnlyBackRight(self) -> None:
        self.backRightMotor.set(0.54)


class TheWB_Xdrive:
    def __init__(self, frontLeftmotor, frontRightmotor, backLeftmotor, backRightmotor):
        self.frontLeftmotor = frontLeftmotor
        self.backLeftmotor = backLeftmotor
        self.frontRightmotor = frontRightmotor
        self.backRightmotor = backRightmotor

        self.Deadband = 0.1
        self.MaxOutput = 0.85

    def setMaxOutput(self, maxOutput: float):
        self.MaxOutput = maxOutput

    def setDeadband(self, deadband: float):
        self.Deadband = deadband

    def driveCartesian(self, xSpeed, ySpeed, zRotation):  # , gyroAngle = 0.0):
        """
        xSpeed: The speed that the robot should drive in its X direction. [-1.0..1.0]
        ySpeed: The speed that the robot should drive in its Y direction. [-1.0..1.0]
        zRotation: The rate of rotation for the robot that is independent of the translation. [-1.0..1.0]
        """
        deadband = self.Deadband

        SmartDashboard.putNumber("Dedband Settting", deadband)
        xSpeed = xSpeed if abs(xSpeed) > deadband else 0.0
        ySpeed = ySpeed if abs(ySpeed) > deadband else 0.0
        zRotation = zRotation if abs(zRotation) > deadband else 0.0

        SmartDashboard.putNumber("xSpeed in TheWB_drivecartesian", xSpeed)
        SmartDashboard.putNumber("ySpeed in TheWB_drivecartesian", ySpeed)
        SmartDashboard.putNumber("zRotation in TheWB_drivecartesian", zRotation)

        # create coding for the mecanum drive kinematics
        base_theta = math.atan2(xSpeed, ySpeed) - math.pi / 4.0
        r = math.hypot(xSpeed, ySpeed)
        cos = math.cos(base_theta)
        sin = math.sin(base_theta)
        max_trig = max(abs(cos), abs(sin))
        leftFront = r * sin / max_trig + zRotation
        rightFront = r * cos / max_trig - zRotation
        leftRear = r * cos / max_trig + zRotation
        rightRear = r * sin / max_trig - zRotation

        # leftFront = r * cos/max_trig + zRotation
        # rightFront = r * sin/max_trig - zRotation
        # leftRear = r * sin/max_trig + zRotation
        # rightRear = r * cos/max_trig - zRotation

        # Limit the toal power to the motors to self.MaxOutput

        maxMagnitude = max(
            abs(leftFront), abs(rightFront), abs(leftRear), abs(rightRear)
        )
        if maxMagnitude > self.MaxOutput:
            leftFront /= maxMagnitude / self.MaxOutput
            rightFront /= maxMagnitude / self.MaxOutput
            leftRear /= maxMagnitude / self.MaxOutput
            rightRear /= maxMagnitude / self.MaxOutput

        SmartDashboard.putNumber("leftFront in TheWB_drivecartesian", leftFront)
        SmartDashboard.putNumber("rightFront in TheWB_drivecartesian", rightFront)
        SmartDashboard.putNumber("leftRear in TheWB_drivecartesian", leftRear)
        SmartDashboard.putNumber("rightRear in TheWB_drivecartesian", rightRear)

        self.frontLeftmotor.set(leftFront)
        self.frontRightmotor.set(rightFront)
        self.backLeftmotor.set(leftRear * 1.1)
        self.backRightmotor.set(rightRear)

        # self.frontLeftmotor_control.with_output(leftFront))
