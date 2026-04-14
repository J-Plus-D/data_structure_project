# Vehicle.py 使用手册

本文档用于说明 [Vehicle.py](Vehicle.py) 中 `Vehicle` 类的设计与使用方法。

## 1. 文件概览

- 文件目标：描述一个车辆对象，管理电量、载重、行驶耗电、充电时间。
- 核心类：`Vehicle`

## 2. 类常量说明

在 [Vehicle.py](Vehicle.py) 中定义了以下类常量：

- `LOAD_CAPACITY_KG = 1500`
  - 车辆最大载重（kg）。
- `AVERAGE_SPEED_KMH = 65`
  - 车辆平均速度（km/h）。
- `CHARGE_SECONDS_PER_KM = 0.4`
  - 充电速度：每补充 1km 对应电量需要 0.4 秒。

## 3. 构造函数

### 3.1 函数签名

```python
def __init__(self, width, current_battery=None, current_load=0.0, energy_per_km=1.0)
```

### 3.2 参数说明

- `width (float)`
  - 地图宽度，用于计算电量上限。
  - 电量上限计算公式：
  $$\text{battery\_capacity} = \text{width} \times 1.5$$
- `current_battery (float | None)`
  - 初始电量。若为 `None`，则默认满电。
- `current_load (float)`
  - 初始载重（kg），默认 `0.0`。
- `energy_per_km (float)`
  - 每公里耗电量，默认 `1.0`。

### 3.3 参数合法性检查

- 当 `width <= 0` 时抛出 `ValueError`。
- 当 `energy_per_km <= 0` 时抛出 `ValueError`。

### 3.4 初始化后自动裁剪范围

- `current_battery` 会被限制在 `[0, battery_capacity]`。
- `current_load` 会被限制在 `[0, load_capacity]`。

## 4. 成员属性说明

实例对象创建后，常用属性如下：

- `battery_capacity`：电量上限。
- `load_capacity`：载重上限（固定 1500kg）。
- `current_battery`：当前电量。
- `current_load`：当前载重。
- `energy_per_km`：每公里耗电量。
- `average_speed`：平均速度（65km/h）。
- `charge_speed`：充电速度（0.4 秒 / km）。

## 5. 方法说明

### 5.1 `set_current_battery(battery)`

- 功能：直接设置当前电量。
- 行为：自动限制到 `[0, battery_capacity]`。
- 返回值：更新后的 `current_battery`。

### 5.2 `set_current_load(load)`

- 功能：直接设置当前载重。
- 行为：自动限制到 `[0, load_capacity]`。
- 返回值：更新后的 `current_load`。

### 5.3 `drive(distance_km)`

- 功能：按里程耗电。
- 计算公式：
  $$\text{consumption} = \text{distance\_km} \times \text{energy\_per\_km}$$
- 行为：`current_battery = max(0, current_battery - consumption)`。
- 异常：`distance_km < 0` 时抛出 `ValueError`。
- 返回值：行驶后的 `current_battery`。

### 5.4 `add_load(delta_kg)`

- 功能：增减载重。
- 规则：
  - `delta_kg > 0`：装货。
  - `delta_kg < 0`：卸货。
- 行为：自动限制到 `[0, load_capacity]`。
- 返回值：更新后的 `current_load`。

### 5.5 `get_charge_time_seconds()`

- 功能：计算从当前电量充满所需时间（秒）。
- 约定：1 电量单位对应 1km。
- 计算步骤：
  1. `need_km = battery_capacity - current_battery`
  2. `time_sec = need_km * charge_speed`
- 返回值：充满所需时间（秒）。

### 5.6 `charge_to_full()`

- 功能：计算充电时间并将电量设为满电。
- 返回值：本次充电所需时间（秒）。

### 5.7 `__repr__()`

- 功能：定义对象的调试显示字符串。
- 常见触发场景：`repr(obj)`、控制台直接查看对象、容器打印对象时。

## 6. 使用示例

```python
from Vehicle import Vehicle

# 1) 创建车辆对象
car = Vehicle(width=200)  # 电量上限 = 200 * 1.5 = 300
print(car)

# 2) 行驶 30km
left_battery = car.drive(30)
print("行驶后电量:", left_battery)

# 3) 装载 500kg
cur_load = car.add_load(500)
print("当前载重:", cur_load)

# 4) 卸载 200kg
cur_load = car.add_load(-200)
print("当前载重:", cur_load)

# 5) 计算充满所需时间（秒）
need_sec = car.get_charge_time_seconds()
print("充满需要(秒):", need_sec)

# 6) 执行充满
used_sec = car.charge_to_full()
print("实际充电(秒):", used_sec)
print(car)
```

## 7. 注意事项

- 当前实现将“电量单位”和“km”按 1:1 对应，用于简化仿真。
- 若后续要接真实能耗模型，可优先扩展 `energy_per_km` 或在 `drive` 中加入速度、负载、路况影响。
- 若业务要求“初始化载重必须为 0，不允许传入初始载重参数”，可将构造函数改为移除 `current_load` 参数并固定为 0。
