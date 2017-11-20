## Project: Search and Sample Return
### Writeup Template: You can use this file as a template for your writeup if you want to submit it as a markdown file, but feel free to use some other method and submit a pdf if you prefer.

---


**The goals / steps of this project are the following:**  

**Training / Calibration**  

* Download the simulator and take data in "Training Mode"
* Test out the functions in the Jupyter Notebook provided
* Add functions to detect obstacles and samples of interest (golden rocks)
* Fill in the `process_image()` function with the appropriate image processing steps (perspective transform, color threshold etc.) to get from raw images to a map.  The `output_image` you create in this step should demonstrate that your mapping pipeline works.
* Use `moviepy` to process the images in your saved dataset with the `process_image()` function.  Include the video you produce as part of your submission.

**Autonomous Navigation / Mapping**

* Fill in the `perception_step()` function within the `perception.py` script with the appropriate image processing functions to create a map and update `Rover()` data (similar to what you did with `process_image()` in the notebook). 
* Fill in the `decision_step()` function within the `decision.py` script with conditional statements that take into consideration the outputs of the `perception_step()` in deciding how to issue throttle, brake and steering commands. 
* Iterate on your perception and decision function until your rover does a reasonable (need to define metric) job of navigating and mapping.  

[//]: # (Image References)

[image1]: ./misc/rover_image.jpg
[image2]: ./calibration_images/example_grid1.jpg
[image3]: ./calibration_images/example_rock1.jpg 

## [Rubric](https://review.udacity.com/#!/rubrics/916/view) Points
### Here I will consider the rubric points individually and describe how I addressed each point in my implementation.  

---
### Writeup / README

#### 1. Provide a Writeup / README that includes all the rubric points and how you addressed each one.  You can submit your writeup as markdown or pdf.  

You're reading it!

### Notebook Analysis
#### 1. Run the functions provided in the notebook on test images (first with the test data provided, next on data you have recorded). Add/modify functions to allow for color selection of obstacles and rock samples.

To allow for color selection of obstacles and rocks samples, I created the functions, detect_obstacles and find_rocks. For detecting obstacles, I used the ground thresh (160, 160, 160) and select only the pixels that are darker than the navigable terrain. For detecting rocks, I used yellow, rgb(110,110,50) as the threshold.  
```
def detect_obstacles(img, rgb_thresh=(160, 160, 160)):
    # Create an array of zeros same xy size as img, but single channel
    color_select = np.zeros_like(img[:,:,0])
    # Require that each pixel be above all three threshold values in RGB
    # above_thresh will now contain a boolean array with "True"
    # where threshold was met
    above_thresh = (img[:,:,0] < rgb_thresh[0]) \
                & (img[:,:,1] < rgb_thresh[1]) \
                & (img[:,:,2] < rgb_thresh[2])
    # Index the array of zeros with the boolean array and set to 1
    color_select[above_thresh] = 1
    # Return the binary image
    return color_select
```
![Obstacle detection](https://i.imgur.com/BxzkhGx.png)

```    
def find_rocks(img, levels=(110, 110, 50)):
    rock_pic = ((img[:,:,0] > levels[0]) \
                & (img[:,:,1] > levels[1])\
                & (img[:,:,2] < levels[2]))
    color_select = np.zeros_like(img[:, :, 0])
    color_select[rock_pic] = 1
    return color_select
```
![Rock detection](https://i.imgur.com/YtxdQUq.png)

#### 1. Populate the `process_image()` function with the appropriate analysis steps to map pixels identifying navigable terrain, obstacles and rock samples into a worldmap.  Run `process_image()` on your test data using the `moviepy` functions provided to create video output of your result. 
In process_image function, I first defined source and destination points for perspective transform, and then applied color threshold to identify navigable terrain, obstacles and rocks. After converting thresholded image pixel values to rover-centric coordd, and converting rover-centric pixel values to world coords, update the worldmap for display. This is the video output:
[Video Output](https://i.imgur.com/dBP9LZM.mp4)


### Autonomous Navigation and Mapping

#### 1. Fill in the `perception_step()` (at the bottom of the `perception.py` script) and `decision_step()` (in `decision.py`) functions in the autonomous mapping scripts and an explanation is provided in the writeup of how and why these functions were modified as they were.
The modification to the perception_step is similar to the changes to process_image function. However, I saved the appropriate pixels to the vision_image and worldmap of the Rover instead.<br>
For the decision_step, I broke the decision tree down into smaller functions. If the rover's mode is 'forward', it will enter the forward_loop function, if the rover's mode is 'stop', it will enter the stop_loop function, and lastly if the rover's mode is 'stuck' it will enter the stuck_loop function. 
In forward_loop function, check if the vision data is available (the number of nav_angles is larger than the threshold to move forward), and if it is not available, go into stop mode. If it is available, continue to move forward.
In stop_loop function, if rover is not stationary, stop moving first. If is it stationary, steer right until more vision data is available and continue into forward mode. 


#### 2. Launching in autonomous mode your rover can navigate and map autonomously.  Explain your results and how you might improve them in your writeup.  

**Note: running the simulator with different choices of resolution and graphics quality may produce different results, particularly on different machines!  Make a note of your simulator settings (resolution and graphics quality set on launch) and frames per second (FPS output to terminal by `drive_rover.py`) in your writeup when you submit the project so your reviewer can reproduce your results.**
<br><br>
Resolution: 1280 x 960 <br>
Graphics Quality: Fantastic <br><br>
The primary metrics of interest are time, percentage mapped, fidelity and number of rocks found. <br>
In order to improve the fidelity of the mapping, I created is_valid_mapping function in perception step to check if the pitch and roll are valid (+/- 1) before updating the worldmap - this allowed the fidelity to stay at around 70% even when making abrupt stops and steering. <br>
In order to improve time, percentage mapped and number of rocks found, I updated the forward moving function to include a bias such that the rover hugs the left wall. Also, to prevent the rover from falsely moving into an obstacle rock (where there is usually navigable terrain in front of and behind the rock), I created a function get_near_nav_angles that ignore the navigable space that are too far away (which usually excludes those behind the rock obstacles).<br> 
This has resulted 98.2% mapped at a 69.4% fidelity, with 6 rocks located in 502s.<br>
In order to avoid obstacles, I have tweaked the constants (such as wall hugging bias, nav_angles distance threshold) and included a stuck condition: when the rover is throttling but its velocity is lower than 0.2 for a long period of time, detect that it is stuck and steer right such that it can move again.<br><br>
The drawback of the current solution is that it is unable to work as accurately when using a different map, since most of the constants are hard-coded for this particular map. Also, if the rock samples appear behind a huge obstacle rock or in narrow areas, the rover is not smart enough to enter - it will turn around instead and miss the rock samples. In order to improve the algorithm, I hope to overcome the above mentioned drawbacks with a better decision tree and collect the rock samples to return them.
<br><br><br>
![Mapping Result](https://i.imgur.com/0nMxw67.png)

