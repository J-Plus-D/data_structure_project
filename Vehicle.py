class Vehicle:
    """车辆类：管理电量、载重、行驶耗电与充电时间。"""

    LOAD_CAPACITY_KG = 1500 #最大载重
    AVERAGE_SPEED_KMH = 65 #平均速度
    CHARGE_SECONDS_PER_KM = 0.4 #充电速度，每充1km里程所需要的电量需要0.4s

    def __init__(self, width, current_battery=None, current_load=0.0, energy_per_km=1.0):
        """
        Args:
            width (float): 地图宽度，用于计算电量上限。
            current_battery (float | None): 当前电量，默认充满。
            current_load (float): 当前载重(kg)。
            energy_per_km (float): 每公里耗电量，默认 1.0。
        """
        if width <= 0:
            raise ValueError("width 必须大于 0")
        if energy_per_km <= 0:
            raise ValueError("energy_per_km 必须大于 0")

        self.battery_capacity = width * 1.5 # 里程等于边长的1.5倍
        self.load_capacity = self.LOAD_CAPACITY_KG # 最大载重固定，为1500kg
        self.current_battery = self.battery_capacity if current_battery is None else float(current_battery) # 初始设置满电，后续根据行驶里程耗电
        self.current_load = float(current_load) # 当前载重
        self.energy_per_km = float(energy_per_km) #每行驶1km，所需要消耗的电量
        self.average_speed = self.AVERAGE_SPEED_KMH #行驶速度，暂时固定
        self.charge_speed = self.CHARGE_SECONDS_PER_KM #充电速度，暂时固定

        self.current_battery = max(0.0, min(self.current_battery, self.battery_capacity)) #确保里程总为正数，且不超过最大里程
        self.current_load = max(0.0, min(self.current_load, self.load_capacity)) #确保负载总为正数，且不超过最大载重

    def set_current_battery(self, battery):
        """直接设置当前电量（自动限制在 [0, 电量上限]）。"""
        self.current_battery = max(0.0, min(float(battery), self.battery_capacity))
        return self.current_battery

    def set_current_load(self, load):
        """直接设置当前载重（自动限制在 [0, 载重上限]）。"""
        self.current_load = max(0.0, min(float(load), self.load_capacity))
        return self.current_load

    def drive(self, distance_km):
        """
        按里程耗电。

        Returns:
            float: 行驶后当前电量。
        """
        if distance_km < 0:
            raise ValueError("distance_km 不能为负数")

        consumption = float(distance_km) * self.energy_per_km #计算这一段路所需要的电量（其实就是里程）
        self.current_battery = max(0.0, self.current_battery - consumption) #目前电量 - 所需要消耗的电量
        return self.current_battery

    def add_load(self, delta_kg):
        """增减载重：正数装货，负数卸货。"""
        self.current_load = max(0.0, min(self.current_load + float(delta_kg), self.load_capacity))
        return self.current_load

    def get_charge_time_seconds(self):
        """
        计算从当前电量充满所需时间（秒）。
        约定 1 电量单位对应 1km，充电速度为每 1km 需要 0.4 秒。
        """
        need_km = self.battery_capacity - self.current_battery
        return need_km * self.charge_speed

    def charge_to_full(self):
        """
        充满电并返回本次充电用时（秒）。
        """
        t = self.get_charge_time_seconds()
        self.current_battery = self.battery_capacity
        return t

    def __repr__(self): #用于调试和查看对象状态的函数
        return (
            f"Vehicle(current_battery={self.current_battery:.2f}/{self.battery_capacity:.2f}, "
            f"current_load={self.current_load:.2f}/{self.load_capacity:.2f}kg, "
            f"average_speed={self.average_speed}km/h)"
        )
