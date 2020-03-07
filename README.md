# PDF Reorderer for bookbinding

This is a command line program to automate re-ordering a PDF in the manner required for bookbinding projects using folded single-sheet 8 or 16 page signatures (AKA "gatherings"). If the PDF is not evenly divisable by 16, blank pages are written and inserted into the PDF in whichever positions are required to keep blank pages together in the rear of book after folding. See [here](https://www.designersinsights.com/designer-resources/understanding-and-working-with-print/) for instructions on folding.

At present, only 8- or 16-page signatures are supported. 

_______________________________________

## Usage

This is a single python script that you can run from your terminal. Verify you have Python3 installed:

```command
$ python3 --version
Python3.X.X
```

If you do not, [download the Miniconda distro for python3.x](https://docs.conda.io/en/latest/miniconda.html).

Once you have Python3 download the only other file in this repository ([```reorder.py```](https://github.com/vxxce/pdf-reorderer/blob/master/reorder.py)). You can then open your terminal and run the program with the following commands:

```command
> pip3  install  PyPDF2
>
> python3  filepath/to/your/download/of/reorder.py
``` 
and follow the prompts from there!

## Development

I am hoping to improve this program by
* supporting additional binding formats and styles
* creating a simple web-based GUI
* collating and re-orienting pages to single sheets of variable dimensions.
* reflowing / formatting pdf content to allow for major adjustments to page-dimensions (IMO the standard 8.5 x 11 ratio is not an especially friendly format for most books).

Happy to collaborate if you have any other ideas or want to work on any of the improvements above!
