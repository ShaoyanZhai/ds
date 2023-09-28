import carla
import math

# 定义回调函数来处理车辆状态的更新
def on_vehicle_speed_update(vehicle):
    velocity = vehicle.get_velocity()
    #velocity=velocity.x
    velocity_kmh = 3.6 *velocity.x  # 将速度从m/s转换为km/h
   
    #print(f"车辆ID: {vehicle.id}, 速度: {velocity_kmh:.2f} km/h, RPM: {rpm:.2f}")
    return velocity_kmh

def get_gear(vehicle):
    vehicle_control = vehicle.get_control()

    # Get the current gear
    current_gear = vehicle_control.gear
    return current_gear

# 计算RPM的示例函数
def calculate_rpm(velocity_kmh,gear):
    # 根据车辆的速度和车型特性计算RPM
    # 这是一个示例，实际情况可能更复杂
    wheel_radius = 0.3  # 轮胎半径（根据车型特性设置）
    if gear==-1:
        gear_ratio=2.94
    elif gear==1:
        gear_ratio=4.58
    elif gear==2:
        gear_ratio=2.96
    elif gear==3:
        gear_ratio=1.91
    elif gear==4:
        gear_ratio=1.45
    elif gear==5:
        gear_ratio=1
    elif gear==6:
        gear_ratio=0.75
    else:
        gear_ratio=1    


    #gear_ratio = 3.42  # 齿轮比（根据车型特性设置）
    #speed_ms = velocity_kmh / 3.6  # 将速度从km/h转换为m/s

    # 计算发动机转速
    if speed_ms == 0:
        return 0.0
    else:
        angular_velocity = speed_ms / wheel_radius
        rpm = (angular_velocity * 3600) / (2 * math.pi * gear_ratio)
        print(rpm)
        return rpm

# 连接到Carla服务器
client = carla.Client('localhost', 2000)
client.set_timeout(5.0)

try:
    # 获取世界对象
    world = client.get_world()

    # 获取所有车辆并选择一个进行监控
    vehicle_list = world.get_actors().filter('vehicle.*')
    print(vehicle_list)
    if vehicle_list:
        vehicle_to_monitor = vehicle_list[0]  # 选择第一辆车
        print(f"监控车辆ID: {vehicle_to_monitor.id}")

        # 启用异步模式
        settings = world.get_settings()
        settings.synchronous_mode = True
        world.apply_settings(settings)

        # 添加车辆状态更新回调函数
        #vehicle_to_monitor.on_tick(lambda snapshot: on_vehicle_speed_update(vehicle_to_monitor))

        while True:
            # 在这里可以添加其他处理逻辑
            world.tick()
            velocity_kmh=on_vehicle_speed_update(vehicle_to_monitor)
            gear=get_gear(vehicle_to_monitor)
            rpm=calculate_rpm(velocity_kmh,gear)
            

            

            
finally:
    # 清理并退出
    settings.synchronous_mode = False
    world.apply_settings(settings)

