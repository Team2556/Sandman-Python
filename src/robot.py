#!/usr/bin/env python3
#
# Copyright (c) FIRST and other WPILib contributors.
# Open Source Software; you can modify and/or share it under the terms of
# the WPILib BSD license file in the root directory of this project.
#

import wpilib
from wpilib import SmartDashboard, Field2d
import wpilib.drive

# import rev
# from pyfrc.physics.drivetrains import MecanumDrivetrain
import commands2
from commands2 import CommandScheduler
import wpimath
from wpimath.geometry import Translation2d, Rotation2d
from constants import DriveConstant, OIConstant, TurretConstant

# import phoenix5
# import math
from subsystems import turret
from subsystems.drivetrain import DriveTrain
from subsystems.cannon import Cannon
from subsystems.turret import Turret

# endregion Helper functions
class MyRobot(commands2.TimedCommandRobot):
    def robotInit(self):
        """
        This function is called upon program startup and
        should be used for any initialization code.
        """
        CommandScheduler.getInstance().run()
        self.timer = wpilib.Timer()

        # region tie ins
        self.robotDrive = DriveTrain()
        self.cannon = Cannon()
        self.turret = Turret()

        self.driverController = commands2.button.CommandXboxController(
            OIConstant.kDriver1ControllerPort
        )
        # Configure the button bindings
        self.ConfigureButtonBindings()

        # endregion tie ins
        self.robotDrive.setDefaultCommand(
            commands2.cmd.run(
                lambda: self.robotDrive.driveWithJoystick(self.driverController),
                self.robotDrive,
            )
        )
        self.cannon.setDefaultCommand(
            commands2.cmd.run(lambda: self.cannon.stop(), self.cannon)
        )
        self.turret.setDefaultCommand(
            commands2.cmd.run(lambda: self.turret.stop_rotate(), self.turret)
        )

        # region SmartDashboard init

        self.field = Field2d()
        SmartDashboard.putData("Field", self.field)  # end up viewing in Glass
        SmartDashboard.putData(CommandScheduler.getInstance())
        # endregion SmartDashBoard init

    def autonomousInit(self):
        """This function is run once each time the robot enters autonomous mode."""
        self.timer.restart()

    def autonomousPeriodic(self):
        """This function is called periodically during autonomous."""

    def teleopInit(self):
        """This function is called once each time the robot enters teleoperated mode."""
        # if self.autonomousCommand is not None:
        #     self.autonomousCommand.cancel()

    def teleopPeriodic(self):
        """This function is called periodically during teleoperated mode."""
        commands2.cmd.runOnce(lambda: self.robotDrive.halt())

    def testInit(self):
        """This function is called once each time the robot enters test mode."""
        commands2.CommandScheduler.getInstance().cancelAll()

    def testPeriodic(self):
        """This function is called periodically during test mode."""

    def end(self):
        """This function is called ?? ever"""
        self.robotDrive.driveCartesian(0, 0, 0, 0)
        self.cannon.stop()  # may want to change thsi to let out air??
        commands2.CommandScheduler.getInstance().cancelAll()
        raise Exception("Robot Code Ended")

    def ConfigureButtonBindings(self):
        # OnlyFrontLeft = commands2.SequentialCommandGroup(
        #     commands2.cmd.run(lambda: self.robotDrive.OnlyFrontLeft()).raceWith(
        #         commands2.WaitCommand(2.2)
        #     )
        # )
        # self.driverController.x().onTrue(OnlyFrontLeft)

        # OnlyFrontRight = (
        #     commands2.cmd.run(lambda: self.robotDrive.OnlyFrontRight())
        #     .raceWith(commands2.WaitCommand(1.2))
        #     .andThen(commands2.WaitCommand(0.5))
        #     .andThen(
        #         commands2.cmd.run(lambda: self.robotDrive.OnlyFrontRight()).raceWith(
        #             commands2.WaitCommand(1.2)
        #         )
        #     )
        # )
        # self.driverController.y().onTrue(OnlyFrontRight)

        # OnlyBackLeft = (
        #     commands2.cmd.run(lambda: self.robotDrive.OnlyBackLeft())
        #     .raceWith(commands2.WaitCommand(0.7))
        #     .andThen(commands2.WaitCommand(0.5))
        #     .andThen(
        #         commands2.cmd.run(lambda: self.robotDrive.OnlyBackLeft()).raceWith(
        #             commands2.WaitCommand(0.7)
        #         )
        #     )
        #     .andThen(commands2.WaitCommand(0.5))
        #     .andThen(
        #         commands2.cmd.run(lambda: self.robotDrive.OnlyBackLeft()).raceWith(
        #             commands2.WaitCommand(0.7)
        #         )
        #     )
        # )
        # self.driverController.a().onTrue(OnlyBackLeft)

        # OnlyBackRight = (
        #     commands2.cmd.run(lambda: self.robotDrive.OnlyBackRight())
        #     .raceWith(commands2.WaitCommand(0.4))
        #     .andThen(commands2.WaitCommand(0.35))
        #     .andThen(
        #         commands2.cmd.run(lambda: self.robotDrive.OnlyBackRight()).raceWith(
        #             commands2.WaitCommand(0.4)
        #         )
        #     )
        #     .andThen(commands2.WaitCommand(0.35))
        #     .andThen(
        #         commands2.cmd.run(lambda: self.robotDrive.OnlyBackRight()).raceWith(
        #             commands2.WaitCommand(0.4)
        #         )
        #     )
        #     .andThen(commands2.WaitCommand(0.35))
        #     .andThen(
        #         commands2.cmd.run(lambda: self.robotDrive.OnlyBackRight()).raceWith(
        #             commands2.WaitCommand(0.4)
        #         )
        #     )
        # )
        # self.driverController.b().onTrue(OnlyBackRight)

        # connon Firing
        fire_cannon = commands2.cmd.run(lambda: self.cannon.fire()).raceWith(
            commands2.WaitCommand(0.2)
        )

        # section Turret

        rotate_right = commands2.cmd.run(
            lambda: self.turret.move_rotate(TurretConstant.kDefault_rotate_speed),
            self.turret,
        )
        rotate_left = commands2.cmd.run(
            lambda: self.turret.move_rotate(-TurretConstant.kDefault_rotate_speed),
            self.turret,
        )

        # self.driverController.rightBumper().onTrue(fire_cannon)
        self.driverController.leftTrigger().whileTrue(rotate_left)
        self.driverController.rightTrigger().whileTrue(rotate_right)

        # end section
