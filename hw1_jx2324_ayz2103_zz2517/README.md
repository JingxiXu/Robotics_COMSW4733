This is a Lab 1 submission for group __21__

## Team Members
Jingxi Xu (jx2324), Aryeh Yonatan Zapinsky (ayz2103), Zhang Zhang (zz2517)

Robot Name: Mark 38

## Question 1
Done. 

## Question 2
Done. Code implementation is found in dancing.py. 

The algorithm uses `randint()` function in random module to generate random numbers which corresponding to different movements of GoPiGo. We check the generated number at each iteration to ensure distinct consecutive dance moves. Each dance move lasts for a random period until Mark 38 decides it's time to stop. To ensure the dancing stops after 20 seconds, at each iteration, the algorithm will check the available time for that movement and modify the time for the final movement.


## Question 3
Done. Code implementation is found in sensor_accuracy.py. 

We first use `servo(104)` to set the sensor facing stright forward, sleep for 3 seconds to let the sensor finish rotating, and then use `us_dist(15)` to get the distances, shown as follows:

| Actaul Distance (in _cm_) | Measured Distance (in _cm_) |
| :---: |:---:|
| 5  | 5  | 
| 30 | 37 |  
| 60 | 76 |  

From the table, we can see there is relation between the actual distance and the measured distance, which is roughly computed as: 

ActualDist = MeasuredDist / 1.29

We will then use this equation to correct the raw measurements from the robot for the following tasks.

## Question 4
Done. Code implementation is found in beam_width.py. The beam width in degrees is 35.

We let Mark 38 scan a thin, long and wooden chopstick (only rotating the ultrasonic sensor using `servo()`) which is perpendicular to the ground where the robot stands. The chopstick can be regarded as a zero-width line. We rotate the servo from 0 degree to 180 degrees and record the degrees when the chopstick enters the beam and when the chopstick leaves the beam. The difference between these two values is the beam width.

## Question 5
Done. Code implementation is found in locate_object.py. 

We rotate Mark 38, while fixing the direction of the ultrasonic sensor, until the object is detected. Then it stops rotating and starts approaching the object in 1cm increments. Mark 38 keeps approaching the object until the object disapears from the beam or it has reached within 20cm of the object. If it stops approaching because the object dispears from the beam, Mark 38 will rotate and find the object again and then repeat the process. Mark 38 stops when it is located 20cm from the object.
