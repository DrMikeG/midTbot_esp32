# Python processing

## 7th May 2020 ##

Read the file line by line

My file contains two layers, which are represented as groups <g> tags - this allows me to compare the edited and unedited porition - although my clumbsy edited actually edits both sections, and I use cut and paste to 'fix' one to be unedited afterwards.

Paths look like this.
The m is move to, 
the little c means this is a relative, polybezier.
the z at the end means closed
there are a few with h or v in, which is something I don't copy with yet.

To start with, I just counted the , but smaller area paths can still have high complexity
Then I tried to count the maxium displacement - this worked ok, but favoured long thing over round areas
Then I tried to estimate the area, treating the coordinates as vertices - this works pretty well, but makes some mistakes I don't yet understand

I am going to try and do a better approximation:


<path
       style="fill:none;stroke:#ff0000;stroke-width:4.75441"
       d="m 4644.4095,-2548.3896 c 0,-3.5888 5.4618,-17.2226 12.1128,-30.2972 16.7193,-32.8657 19.9951,-59.5102 8.5584,-69.6047 -13.504,-11.9192 -53.5095,-18.6102 -83.053,-13.8908 -28.3172,4.5236 -30.4106,3.9963 -26.3313,-6.6333 2.1808,-5.684 10.6209,-7.3367 37.4652,-7.3367 38.9853,0 61.8412,5.1796 73.2651,16.6034 7.1663,7.1665 8.4357,6.2244 16.8068,-12.4727 8.8095,-19.6765 33.7221,-53.1188 52.8358,-70.926 10.1483,-9.4546 39.2933,-24.6833 50.9526,-26.6237 28.2093,-4.6946 40.3298,-3.7252 38.5725,3.0851 -1.0117,3.9224 -2.2978,10.3409 -2.8578,14.2633 -0.5601,3.9224 -2.5303,14.6198 -4.3793,23.7721 -1.8485,9.1522 -3.8882,20.3226 -4.5319,24.823 -1.9417,13.5655 -7.1421,15.0562 -10.1878,2.9204 -1.5756,-6.2776 -0.7303,-20.9135 1.8785,-32.5243 2.6087,-11.6108 4.1434,-21.7105 3.4103,-22.4436 -0.7331,-0.7332 -11.8451,0.1022 -24.6935,1.8561 -16.9475,2.3136 -26.8206,6.886 -35.9652,16.6559 -6.9329,7.4068 -14.5038,13.4669 -16.8244,13.4669 -10.009,0 -34.8409,51.7177 -42.2316,87.9566 -4.2666,20.9194 -13.2477,48.2348 -19.9581,60.7007 -13.6166,25.2942 -24.877,37.373 -24.8441,26.6495 z"
       id="path20026" />