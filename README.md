# REAL TIME FACE MASK DETECTION PROJECT
Graduation project: Face mask detection based AI 
by: 
Abedallah Joulany &
Mohamad Ektelat
Moderator:
Sagiv Tuvia
College: 
Hadassah academic college

# About the project
When the covid-19 spread, one of the ways to limit its spread was to were a mask, but not all people committed to wearing it or wearing it correctly.

- In the project we decided to build a real time system to detect by a camera, person who is not wearing a mask or not wearing it correctly, and if the person is found in our database the system was able to recognize him, it will show his details and send him a mail to wear a mask.  

# Example
![image](https://user-images.githubusercontent.com/59060418/200169243-03aae822-f79b-49f2-99ca-171ccb81272e.png)

![image](https://user-images.githubusercontent.com/59060418/200169213-752f31ad-e298-4599-8a86-7bd0e5f609af.png)

![image](https://user-images.githubusercontent.com/59060418/200169249-70c242be-7cc9-4964-8ef3-a7a52b62b059.png)

# showing the details
![image](https://user-images.githubusercontent.com/59060418/200169302-38b06b9f-f2f9-4244-a51f-4d7eb2f6cb18.png)

# Detection
The detection goes through several stages
- The System detect faces in picture
  In this part we used a built-in model to detect faces
- The System determines if the face is with mask or not.
- The System checks if mouth or nose found in picture to determine wither person is wearing mask correctly
  in this stage we encounterd some difficulties in determining if mask is weard correctly so that was our simple solution.
- showing the result on screen.
- Not wearing a mask

![image](https://user-images.githubusercontent.com/59060418/202166062-c1e8aa61-a9f1-45a8-aafe-2b9590992e80.png)

- Wearing mask wrong

![image](https://user-images.githubusercontent.com/59060418/202166133-3d50a790-28f0-4726-abce-de400abb6d44.png)

# Recognition
The recognition goes through several stages
- If person detected without the mask In the detection stage, the picture is sent to a thread to do the recognition
- The thread finds the 128 measurements of the face and compares it with pictures in our dataBase where we saved persons deatils and measurments.
- If person is found we get his details otherwise we get unknown.
- Then the details are passed to another thread to send the email to that person.

# More System Features

- The System have a Page to add people in real time where you can enter the details and the pictures of the person

![WhatsApp Video 2022-10-19 at 20 46 351 - frame at 0m21s](https://user-images.githubusercontent.com/59060418/202843403-b4da6588-3246-4318-ba08-875b14308b5e.jpg)

- The System works on both linux and windows.
- After a lot of research we figured out that face recognition on linux is 10x faster than windows
- Windows results

![image](https://user-images.githubusercontent.com/59060418/202843520-e24fcec0-68b3-4041-ace8-46965aa79112.png)

- Linux Results

![image](https://user-images.githubusercontent.com/59060418/202843535-a8d03612-35a3-4b82-976d-548f5ae051c7.png)

# Summary
I will put some links for videos of the project

- recognitoin while face mask is off
https://youtu.be/OI4WMvcRRWc

- Wearing mask incorrectly 
https://youtu.be/bZvnnbNnp0E

- windows result with delay
https://youtu.be/oon7kAhHWUw

# Thanks
Thanks for my partner mohammad for the teamwork, and thanks for sagiv tuvia for the guidence.
