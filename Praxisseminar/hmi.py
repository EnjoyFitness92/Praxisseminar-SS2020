"""
IN BEARBEITUNG

Praxisseminar hmi.py
"""

from minicps.devices import HMI
from utils import Praxisseminar_test_logger
from utils import STATE, PLC1_DATA, PLC1_PROTOCOL, PLC1_ADDR

import get_ip

#import sys
import time


HMI_ADDR = get_ip()

# constant tag addresses
SENSOR_1 = ('SENSOR', 1)
MOTOR_1 = ('MOTOR', 1)


class PHMI(HMI):

    """Praxisseminar HMI.

    HMI provides:
        - state APIs: e.g., get a water level indicator
        - network APIs: e.g., monitors a PLC's tag
    """


    def main_loop(self, sleep=0.5):
        """HMI main loop.

        :param float sleep: second[s] to sleep after each iteration
        """

        # die HMI Addresse zurückgeben
        print 'DEBUG: die Adresse des aktuellen HMI lautet: ' + HMI_ADDR
        Praxisseminar_test_logger.debug('DEBUG: die Adresse des aktuellen HMI lautet: ' + HMI_ADDR)

        sec = 0
        while(sec < 1):

            rec_s11 = self.receive(SENSOR_1, PLC1_ADDR)
            rec_m11 = self.receive(MOTOR_1, PLC1_ADDR)
            Praxisseminar_test_logger.debug('Sensor_1: ' + rec_s11)
            Praxisseminar_test_logger.debug('Motor_1: ' + rec_m11)



            print "Sie haben folgende Optionen: "
            print
            eingabe = str(input("Auslesen Status: Taste 1/ Geschwindigkeit einstellen: Taste 2/ Ein-/Ausschalten: Taste 3/ Programm beenden: Taste 99 "))

            # evtl doch auf switch ... case umsteigen - geht nicht so wie ich mir das vorstelle

            # Status abfragen (Ein
            if eingabe == '1':
                motor = self.receive(MOTOR_1, PLC1_ADDR)
                print "DEBUG plc1 erhält motor: " + motor
                Praxisseminar_test_logger.debug('Motor_1: ' + motor)

                # wenn mit eigenem Status-Bereich gearbeitet wird
                #self.send(MOTOR_1, motor, HMI_ADDR)

                if motor == 1:
                    print 'DEBUG plc1 motor: An'
                elif motor == 0:
                    print 'DEBUG plc1 motor: Aus'
                print
                Praxisseminar_test_logger.debug('Motor_1: ' + motor)

            elif eingabe == '2':
                motor = self.receive(MOTOR_1, PLC1_ADDR)
                print "DEBUG plc1 erhält motor: " + motor
                Praxisseminar_test_logger.debug('Motor_1: ' + motor)

                # siehe Eingabe '1'

                if motor == 1:
                    sensor = float(self.receive(SENSOR_1, PLC1_ADDR))
                    print 'DEBUG plc1 motor: An mit der Geschwindigkeit' + sensor
                    Praxisseminar_test_logger.debug('Sensor_1: ' + sensor)

                    # Wollen Sie die Geschwindigkeit verändern? Wie hoch soll die Geschwindigkeit sein (Rahmen der Geschwindigkeit anpassen)
                    change = input("Wollen Sie die Geschwindigkeit veraendern? J/N")

                    if change == "J" or change == "j":
                        new_vel = float(input("Geben Sie die neue Geschwindigkeit ein: "))
                        self.set(SENSOR_1, new_vel)
                        self.send(SENSOR_1, new_vel, PLC1_ADDR)
                        print 'DEBUG plc1 motor: An mit neuer Geschwindigkeit' + new_vel
                        Praxisseminar_test_logger.debug('Sensor_1: ' + new_vel)

                    elif change == "N" or change == "n":
                        break

                elif motor == 0:
                    print 'DEBUG plc1 motor: Aus'
                print
                Praxisseminar_test_logger.debug('Motor_1: ' + motor)

            elif eingabe == '3':
                motor = self.receive(MOTOR_1, PLC1_ADDR)
                print "DEBUG plc1 erhält motor: " + motor
                Praxisseminar_test_logger.debug('Motor_1: ' + motor)

                if motor == 1:
                    onoff = input("Wollen Sie den Motor aus oder einschalten? Aus = 0 /Ein = 1")

                    if onoff == 0:
                        self.send(MOTOR_1, onoff, PLC1_ADDR)
                    elif onoff == 1:
                        self.send(MOTOR_1, onoff, PLC1_ADDR)

            time.sleep(sleep)

            sec += 1



if __name__ == "__main__":

    # notice that memory init is different form disk init
    phmi = PHMI(
        name='phmi',
        state=STATE,
        protocol=PLC1_PROTOCOL,
        memory=PLC1_DATA,
        disk=PLC1_DATA)
