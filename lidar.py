from rplidar import RPLidar, RPLidarException
# import smbus2 as smbus
import math

# bus = smbus.SMBus(1)
# address = 8

# def send_data_to_arduino(data):
#     bus.write_byte(address,data)
#     print("raspberry pi sent: ", data)

lidar = RPLidar('COM10')

lidar.__init__('COM10', 256000, 3, None)

lidar.connect()
print('lidar connected')
info = lidar.get_info()
print(info)

health = lidar.get_health()
print(health)


try:

    for i, scan in enumerate(lidar.iter_scans()):

        one_sent = False
        last_angle = None
        
        for d in scan:
            angle = d[1]
            distance = d[2] / 10

            if 299 <= angle <= 301:

                uzaklik = distance / 2
                sol_son_deger = uzaklik * math.sqrt(3)

            if 59 <= angle <= 61:

                uzaklik = distance / 2
                sag_son_deger = uzaklik * math.sqrt(3)

                x = sol_son_deger - sag_son_deger
                if (abs(sol_son_deger - sag_son_deger)) <= 4:
                    print(f'aracın sol değeri: {sol_son_deger}, sağ değeri: {sag_son_deger}, x = {x}')
                    print("Araç düz gitsin")
                elif (sol_son_deger - sag_son_deger) >= 4:
                    print(f'aracın sol değeri: {sol_son_deger}, sağ değeri: {sag_son_deger}, x = {x}')
                    print("Araç sola gitsin")
                elif (sag_son_deger - sol_son_deger) >= 4:
                    print(f'aracın sol değeri: {sol_son_deger}, sağ değeri: {sag_son_deger}, x = {x}')
                    print("Araç sağa gitsin")
                else:
                    print("Lidar değer okumuyor")


                '''if (d[2] / 10) <= 50:
                    one_sent = True
                    print(1)
                    send_data_to_arduino(1)
                    break
                
                else:
                    one_sent = False'''
            else:
                print("Lidar değer okumuyor")
            if last_angle is not None and abs((last_angle - d[1]) % 360) > 355:
                one_sent = False
            
            last_angle = d[1]
            
        # if not one_sent:
        #     print(0)
        #     send_data_to_arduino(0)
        #     one_sent = False

        if False:
            lidar.stop()
            lidar.stop_motor()
            lidar.disconnect()
            break
        
except KeyboardInterrupt as err:
    print('key board interupt')
    lidar.stop()
    lidar.stop_motor()
    lidar.disconnect()

except RPLidarException as err:
    print(err)
    lidar.stop()
    lidar.stop_motor()
    lidar.disconnect()
    
except AttributeError:
    print('hi attribute error')
