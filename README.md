<h1>Python Borehole DXF Creator</h1>

### This code reads a xlsx file containing information about standard penetration test (SPT) and creates a DXF file with the drawing of all the boreholes listed on it with a legend.

<img src=/static/DXF_log_image.png>

<h3>XLSX file (borehole_example.xlsx)</h3>

<p1>This is the file that will be used to store the borehole data you want to draw. The columns needed to run the program are listed in the table below with an example. </p1>

| borehole_name | initial_depth | final_depth | material |
| --- | --- | --- | --- |
| BH-01 | 0 | 1 | clay 1 |
| BH-01 | 1 | 5,5 | clay 2 |
| BH-02 | 0 | 2 | clay 1 |
| BH-02 | 2 | 6 | rock |

<p1>The guidelines to create the table are pretty simple. Each line of the file represents a layer of a different material, with the *initial_depth* and the *final_depth* of a given borehole. Every time the material or the borehole changes, you add a new line. The 4  columns must be filled in order to run the program.</p1>


<p1>⚠️  The name of the columns **MUST NOT BE CHANGED!!!** The program uses it to locate all the information needed to the drawing. I strongly recommend you to download the borehole_example.xlsx and just modify the data below the header.</p1>

<p1>⚠️  The depth must be indicated as positive numbers. The program will convert it to negative and draw it properly in the cartesian plan, considering 0.0 as the ground elevation of all boreholes.</p1>
<br> 
<br>  
<h3>Layers</h3>

<p1>The program will create one layer for each material in the data source, with the same name of the material. These layers will hold the **HATCH** DXF entities. Also, the *"information"* layer will be used to store the box with the name of the borehole (text and polyline entities). The layer *"0"* will be used do draw the polylines of the squares surrounding the HATCH entities.</p>
<br>  
<h3>Colors</h3>

<p1>The program uses the default <a href="https://ezdxf.readthedocs.io/en/stable/concepts/aci.html?highlight=color%20system">AutoCad Color Index</a> to differentiate the materials. The first material will use color 1, the second color 2 and so on. For this reason, the limit of materials that you can use in the same file is 255. The colors of the materials can, later on, be easily changed by changing the color of it's layer.</p>
<br>  
<h3>Associative HATCH</h3>

<p1>The program associates the polylines with the hatch entities, so you can easily change the depth of the materials in a CAD application as showed bellow.</p1>

<img src=/static/DXF_log_associative.png>
<br> 
<h3>Requirements</h3>
 
<p1>The requirements for the program can be found in the file requirements.txt</p1>
<br>  
<br>  
<h3>How to Run</h3>

<p1>Run the program via CMD or IDLE and select the xlsx file that has the borehole data in the window that just opened. The drawing will be saved in the same path as the python main.py file.</p1>
<br>  
<br>  
<h3>Example</h3>

<p1>The borehole_example.xlsx can be used to test the program. The result must be equal to the image listed bellow the title</p1>

<h6>If this was usefull for you, please consider commenting on my <a href="https://www.linkedin.com/in/marcus-paulo-zucareli-dias-rodrigues-734690105/?locale=en_US">LinkedIn Profile</a></h6>

