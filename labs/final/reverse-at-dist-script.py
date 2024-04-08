scan = rc.lidar.get_samples()
lidar_closest_in_safety = rc_utils.get_lidar_closest_point(scan, (270,90))
if lidar_closest_in_safety[1] < 10:
    speed = -1