# Minimize Bounding Box Volume - Blender Addon
![](images/Addon%20Doc%20-%20MinBound%20Santa.png)

## Installation
1. Right click [**this link**](https://raw.githubusercontent.com/japuzen/bpy-minboundbox/master/MinimizeBoundBoxAddon.py) and click *Save Link As* to download the Python file.
2. In Blender, go to *Edit > Preferences*.

![](https://github.com/japuzen/bpy-pack/blob/master/images/Addon%20Doc%20-%20Edit>Preferences.png)

3. In *Addons* click *Install* and find the *MinimizeBoundBoxAddon.py* file.

![](https://github.com/japuzen/bpy-pack/blob/master/images/Addon%20Doc%20-%20Addon%20Install.png)

4. Click the checkbox to the left of the addon to enable it.

## Usage
1. Select the objects.
2. Click the ***Minimize Bounding Box*** operator at the bottom of the ***Object*** dropdown menu. You can also the *Search* function in Blender to find the operator.

![](images/Addon%20Doc%20-%20Object%20Dropdown.png)

![](images/Addon%20Doc%20-%20Min%20Bound%20Operator.png)

## Info
&nbsp;&nbsp;&nbsp;&nbsp;The Minimize Bounding Box add-on, as the name suggests, automatically minimizes the bounding box volume of selected objects in Blender. It will take several seconds to process each object. Run time depends on the complexity of the objects, meaning objects with higher poly counts will take longer to process. There is a step in the add-on that will decimate the object and work with a lower poly count duplicate to counteract this.

<img src="images/Addon%20Doc%20-%20MinBound%20Suzanne.png" height="75%" width="75%" align="center">
<img src="images/Addon%20Doc%20-%20MinBound%20L.png" height="75%" width="75%" align="center">
