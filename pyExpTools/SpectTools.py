from cycler import cycler, Cycler
from typing import List
from functools import reduce
from multipledispatch import dispatch
import matplotlib.pyplot as plt
import matplotlib.axes as mplAx
import matplotlib.figure as mplFig
import matplotlib as mpl
import pandas as pd
import pathlib
import parse
import json

class plotConf:
    """
    A class which configures a matplotlib plot according to a description

    Attributes
    ----------
    title: str
        The title wanted for the graph

    axis_titles: list(str)
        A list of the axis titles (limited to length 2)

    axis_ranges: list(float, float)
        A list of float pairs which defines the range of graphing (limited to length 2)
    
    style_sheet (optional): str
        A string which represents the style sheet that matplotlib will use under this configuration. Much be one of the available styles

    color_cycle (optional): cycler 
        A color cycle describing the colors / options used for the given graphs

    Methods
    -------
    pre_ops(active_ax: matplotlib.axes.Axes): None
        This function applies preplot operations to some set of axes in order to set the color cycler correctly

    post_ops(active_ax: matplotlib.axes.Axes): None
        This function applies postplot operations to some set of axes in order to set the display ranges correctly
    """
    __plotConf_namespace = dict()

    #Constructors
    @dispatch(namespace = __plotConf_namespace)
    def __init__(self):
        """The Default constructor for the plotConf class"""
        self.__title = None
        self.__axis_titles = [None, None]
        self.__axis_ranges = [[None, None], [None, None]]
        self.__style_sheet = None
        self.__color_cycle = None

    @dispatch(str, list, list, list, Cycler, namespace = __plotConf_namespace)
    def __init__(self, title: str, axis_titles: List[str], axis_ranges: List[List[float]], style_sheet: str = None, color_cycle: Cycler = None):
        """
        This is the main constructor of the plotConf. It builds this class given a small description of what the plot should look like

        Parameters
        ----------
        title: str
            This is the title of the axis you want to style

        axis_titles: List[str]
            This is a list of string giving the titles of the axis you want to operate on. In xyz order

        axis_ranges: List[List[float, float]]
            A list of float pairs which describe the limits on the axis. A pair of Nones does not constrain that axis. In xyz order

        style_sheet: str
            The matplotlib style sheet which should be applied to the graph. Useful for changing basic things about the plot like axis colors and such

        color_cycle: Cycler
            The cycler for the plot. This sets how the graph "chooses" the properties of undefined data. It's a bit complicated but very powerful see here: https://matplotlib.org/3.3.3/tutorials/intermediate/color_cycle.html
        """
        self.__init__()
        self.title = title
        self.axis_titles = axis_titles
        self.axis_ranges = axis_ranges
        self.style_sheet = style_sheet
        self.color_cycle = color_cycle

    #Dealing with the Title attribute
    @property
    def title(self):
        """Returns the current set title"""
        return self.__title

    @title.setter
    def title(self, new_title: str):
        """
        Sets the title for the plot configuration
        
        Parameters
        ----------
        new_title: str
            The new title for the plot configuration
        """
        self.setTitle(new_title)

    def setTitle(self, new_title: str):
        """
        Sets the title for the plot configuration
        
        Parameters
        ----------
        new_title: str
            The new title for the plot configuration
        """
        if (isinstance(new_title, str) | (new_title is None)):
            self.__title = new_title
        else:
            raise TypeError("The new title needs to be a string or None.\nGot: {}".format(type(new_title)))
        return None
    
    #Dealing with the Axis Titles
    @property
    def axis_titles(self):
        """Returns the current set axis titles"""
        return self.__axis_titles

    @axis_titles.setter
    def axis_titles(self, new_titles: List[str]):
        """
        Sets the axis titles for the plot configuration

        Parameters
        ----------
        new_titles: list(str) | maximum length: 2
            The titles for the configured plot as a list of strings
        """
        self.setAxisTitles(new_titles)

    def setAxisTitles(self, new_titles: List[str]):
        """
        Sets the axis titles for the plot configuration

        Parameters
        ----------
        new_titles: list(str) | maximum length: 2
            The titles for the configured plot as a list of strings
        """
        if (not (isinstance(new_titles, list) | isinstance(new_titles, tuple))):
            raise TypeError("The input axis titles need to be in either a list or tuple")

        if (len(new_titles) > 2):
            raise ValueError("The input axis titles can only be at most length 2")

        for index in range(len(new_titles)):
            if (not isinstance(new_titles[index], str)):
                raise ValueError("All of the input axis titles need to be strings. Got: {} at {}".format(type(new_titles[index]), index))
            self.__axis_titles[index] = new_titles[index]
        return None

    #Dealing with the axis ranges
    @property
    def axis_ranges(self):
        """Returns the axis ranges of the plot"""
        return self.__axis_ranges

    @axis_ranges.setter
    def axis_ranges(self, new_ranges: List[List[float]]):
        """
        Sets the axis ranges for the plot configuration

        Parameters
        ----------
        new_ranges: list(float, float) | maximum length: 2
            The new ranges for the configured plot as a list of pair of floats
        """
        self.setAxisRanges(new_ranges)

    def setAxisRanges(self, new_ranges: List[List[float]]):
        """
        Sets the axis ranges for the plot configuration

        Parameters
        ----------
        new_ranges: list(float, float) | maximum length: 2
            The new ranges for the configured plot as a list of pair of floats
        """
        #Error checks
        if (not (isinstance(new_ranges, list) | isinstance(new_ranges, tuple))):
            raise TypeError("The input axis ranges need to be in either a list or tuple")
        if (len(new_ranges) > 2):
            raise ValueError("The input axis titles can only be at most length 2")

        for index in range(len(new_ranges)):
            if (len(new_ranges[index]) != 2):
                raise ValueError("The new axis ranges need to be in pairs. Index {} was not a pair".format(len(new_ranges)))

            if (not (isinstance(new_ranges[index][0], float), isinstance(new_ranges[index][0], int))):
                raise ValueError("The first value in pair at index {} was not a float or integer".format(index))

            if (not (isinstance(new_ranges[index][1], float), isinstance(new_ranges[index][1], int))):
                raise ValueError("The second value in pair at index {} was not a float or integer".format(index))

            self.__axis_ranges[index] = new_ranges[index]
        return None

    #Dealing with the stylesheet
    @property
    def style_sheet(self):
        """Returns the style sheet list"""
        return self.__style_sheet

    @style_sheet.setter
    def style_sheet(self, style_list: List[str]):
        """
        Sets the style sheets to use while plotting the figures

        Parameters
        ----------

        style_list: list(str)
            A list of strings which indicate the style sheets to use
        """
        self.setStyleSheet(style_list)

    def setStyleSheet(self, style_list: List[str]):
        """
        Sets the style sheets to use while plotting the figures

        Parameters
        ----------

        style_list: list(str)
            A list of strings which indicate the style sheets to use
        """
        if style_list is None:
            self.__style_sheet = None
            return None

        if len(style_list) == 0:
            self.__style_sheet = None
            return None

        available_list = plt.style.available

        assert (isinstance(style_list, list) | isinstance(style_list, tuple)), TypeError("The style list needs to be a tuple or list. Got {}".format(type(style_list)))

        for index in range(len(style_list)):
            assert (style_list[index] in available_list), ValueError("All possible styles need to be available. Index {} was not available. Got {}".format(index, style_list[index]))
        
        self.__style_sheet = style_list
        return None

    #Dealing with the color_tool
    @property
    def color_tool(self):
        """Returns the color cycle being used for the configuration"""
        return self.__color_cycle

    @color_tool.setter
    def color_cycle(self, new_cycle: cycler):
        """
        This sets the color cycle of the configuration to help matplotlib choose the colors correctly

        Parameters
        ----------

        new_cycle: cycler
            A cycler from the cycler library which sets the sequence in which colors and other options are selected. Needs to have at least "colors" set
        """
        self.setColorCycle(new_cycle)

    def setColorCycle(self, new_cycle: cycler):
        """
        This sets the color cycle of the configuration to help matplotlib choose the colors correctly

        Parameters
        ----------

        new_cycle: cycler
            A cycler from the cycler library which sets the sequence in which colors and other options are selected. Needs to have at least "colors" set
        """
        #Error checking
        if (not (isinstance(new_cycle, Cycler) | (new_cycle is None))):
            raise TypeError("The new cycle needs to be of class cycler. Got {}".format(type(new_cycle)))

        if (new_cycle is None):
            self.__color_cycle = None
            return None

        #Making sure that color is set in the cycle
        assert("color" in new_cycle.keys), ValueError("The new cycle needs to have the color value set")

        self.__color_cycle = new_cycle
        return None

    #Plot based operations
    def preOps(self, active_ax: mplAx.Axes):
        """
        The preplot operations which are done to some matplot figure in order to present it correctly

        Parameters
        ----------

        active_ax: matplotlib.axes.Axes
            The figure which the configurator is supposed to change and operate on
        """
        if (self.color_cycle is not None):
            active_ax.set_prop_cycle(self.color_cycle)

        if (self.title is not None):
            active_ax.set_title(self.title)

        if (self.axis_titles[0] is not None):
            active_ax.set_xlabel(self.axis_titles[0])

        if (self.axis_titles[1] is not None):
            active_ax.set_ylabel(self.axis_titles[1])

        return None

    def postOps(self, active_ax: mplAx.Axes):
        """
        The postplot operations which are done to some matplot figure in order to present it correctly

        Parameters
        ----------

        active_ax :matplotlib axes
            The figure which the configurator is supposed to change and operate on
        """
        
        if (self.axis_ranges[0][0] is not None and self.axis_ranges[0][1] is not None):
            active_ax.set_xlim(self.axis_ranges[0])

        if (self.axis_ranges[1][0] is not None and self.axis_ranges[1][1] is not None):
            active_ax.set_ylim(self.axis_ranges[1])

        return None

    #<---------------------Operations--------------------->
    def __str__(self):
        """Prints the information for the plot configurator"""
        main_str = "Plot configurator settings\n"

        main_str += "Title: {}\n".format(self.title)

        main_str += "X-axis Title: {}, Y-axis Title: {}\n".format(self.axis_titles[0], self.axis_titles[1])

        main_str += "Axis ranges: {}\n".format(self.axis_ranges)

        if self.style_sheet is not None:
            main_str += "[" + ("{}, " * (len(self.style_sheet) - 1)) + "{}]"
            main_str.format(*self.style_sheet)

        return main_str

    def __eq__(self, value):
        """
        Evaluates the equality of the plot configurator to another plot configurator
        """
        if not isinstance(value, plotConf):
            return NotImplemented("plotConfs can only be equated to other plotConfs")
        
        truth_value = True

        #Stylesheets
        if (len(self.style_sheet) == len(value.style_sheet)):
            for index in range(len(self.style_sheet)):
                truth_value = truth_value and (self.style_sheet[index] == value.style_sheet[index])
        else:
            return False

        #Axis ranges
        for index in range(len(self.axis_ranges)):
            truth_value = truth_value and (self.axis_ranges[index][0] == value.axis_ranges[index][0]) and (self.axis_ranges[index][1] == value.axis_ranges[index][1])

        #Axis Titles
        for index in range(len(self.axis_titles)):
            truth_value = truth_value and (self.axis_titles[index] == value.axis_titles[index])

        #Title
        truth_value = truth_value and (self.title == value.title)

        return truth_value

class SpectExp:
    """
    A class which represents a single spectral experiment output by the oceanview 1.6 software

    Attributes
    ----------
    plotConf: plotConf
        The plot configurator for the graphs this experiment will produce

    data: pandas.dataFrame
        The raw data associate with the spectral experiment

    metaInfo: str
        A list of strings which represents any metadata found in the source file

    sourceFile: Path
        The path to the spectral data file

    outputPath: Path
        Where the plot of this experiment should be saved if it's plotted

    name (optional): str
        A string which names the experiment. Is calculated based on the filename if not specified

    Methods
    -------
    readFile(delim: str = ",", begin_line: str = None, convert_dict: dict = None, col_names: list(str) = None) -> Bool
        Attempts to read in the file for the experiment.

    outputNameGen() -> str
        A method which generates the output name of the file from the name of the experiment

    legendNameGen() -> str
        A method which generates the legend name of the experiment from the name

    nameParser() -> dict
        Parses the input file name into a series of key value pairs which can be used with the name generators

    plot(ax: matplotlib.axes.Axes) -> matplotlib.axes.Axes
        Plots the data according to the plot configurator on the specified ax. If non given then plots it as a complete figure
    
    plot(ax: matplotlib.axes.Axes, config: plotConf) -> matplotlib.axes.Axes
        A version of the plot command which plots with an outside configurator. Useful for using a temporary configuration

    save()
        Plots the data and then saves that information to the output path according to the name generators / set name
    """

    __SpectExp_namespace = dict()

    default_read_dict = {
            "delim": "\t", 
            "begin_line": ">>>>>Begin Spectral Data<<<<<\n", 
            "convert_dict": {"A": "float64", "B": "float64"}, 
            "col_names": ["Wavelength", "Measure"]
        }

    #<---------------------Constructors--------------------->

    @dispatch(namespace = __SpectExp_namespace)
    def __init__(self):
        """
        The default constructor for the SpectExp class. Sets just about everything to None
        """
        self.__plotConf = plotConf()
        self.__data = None
        self.__metaInfo = None
        self.__sourceFile = None
        self.__outputPath = None
        self.__name = None
        self.__saveFormat = "png"
        
    @dispatch(plotConf, (pathlib.Path, str), (pathlib.Path, str), str, namespace = __SpectExp_namespace)
    def __init__(self, config: plotConf, sourceFile: [pathlib.Path, str], outputPath: [pathlib.Path, str], name: str = None):
        """

        Constructs a given Spectral Experiment object using a "default read method". In other words using the most likely saved method for when the experiment was saved

        Parameters
        ----------
        config: plotConf
            The plot configurator used for this experiment

        sourceFile: [pathlib.Path, str]
            The source data file for the experiment. Expects a txt or csv file

        outputPath: [pathlib.Path, str]
            The output path for the experiment

        name: str
            The name of the experiment

        """
        self.__init__(config, sourceFile, outputPath, name, SpectExp.default_read_dict)

    @dispatch(plotConf, (pathlib.Path, str), (pathlib.Path, str), str, dict, namespace = __SpectExp_namespace)
    def __init__(self, config: plotConf, sourceFile: [pathlib.Path, str], outputPath: [pathlib.Path, str], name: str = None, readDict: dict = None):
        """

        Constructs a given Spectral Experiment object using a "default read method". In other words using the most likely saved method for when the experiment was saved

        Parameters
        ----------
        config: plotConf
            The plot configurator used for this experiment

        sourceFile: [pathlib.Path, str]
            The source data file for the experiment. Expects a txt or csv file

        outputPath: [pathlib.Path, str]
            The output path for the experiment

        name: str
            The name of the experiment

        readDict: dict
            A dictionary which describes the input into the "readFile" function. Thereby allowing the user to describe how they want their info file to be processed when reading it into the Spectral Experiment class

        """
        self.__init__()
        self.setPlotConf(config)
        self.setSource(sourceFile)
        self.setOutPath(outputPath)
        self.setName(name)
        self.readFile(delim = readDict["delim"], begin_line = readDict["begin_line"], convert_dict = readDict["convert_dict"], col_names = readDict["col_names"])


    #<---------------------Setters--------------------->

    def setPlotConf(self, newConf: plotConf):
        """
        Sets the plot configurator for this experiment. Effectively this stylizes the plot

        Parameters
        ----------
        newConf: plotConf
            The new plot configurator to be set
        """
        assert isinstance(newConf, plotConf), "The new plot configurator needs to be a plot configurator. Got {}".format(type(newConf))

        self.__plotConf = newConf
        return None

    def setData(self, newData: pd.DataFrame):
        """
        Sets the data of the experiment. Intended to only be used internally but exposed just in case

        Parameters
        ----------
        newData: pandas.DataFrame
            The dataframe to be used as the information for the experiment. Can only have two columns one for the wavelength and the other for the measurement
        """
        assert isinstance(newData, pd.DataFrame), "The new data needs to be a pandas dataframe. Got {}".format(type(newData))

        assert newData.shape[1] == 2, "The new data must have two columns. One for wavelength, the other for the measurement. Got {}".format(newData.shape[0])

        newData.columns = ["Wavelength", newData.columns[1]]
        self.__data = newData
        return None

    def setSource(self, newSource: [pathlib.Path, str]):
        """
        Sets the source file for the experiment

        Parameters
        ----------
        newSource: [pathlib.Path, str]
            The new sourcefile. Automattically converted into a path object
        """
        if (isinstance(newSource, pathlib.PurePath)):
            #If the user gave a path as input
            if (not newSource.exists()):
                raise ValueError("The new source file does not exist")
            if (newSource.is_file()):
                assert newSource.suffix in [".txt", ".csv"], "Source file needs to be either a txt file or a csv file. Got {}".format(newSource.suffix)
                self.__sourceFile = newSource
            else:
                raise ValueError("The source path needs to lead to a file")
        elif (isinstance(newSource, str)):
            #If the user gave a string path
            newSource = pathlib.Path(newSource)
            self.setSource(newSource)
        else:
            raise TypeError("Expected a string or path. Got {}".format(type(newSource)))
        return None

    def setOutPath(self, newOutput: [pathlib.Path, str]):
        """
        Sets the output path of the experiment

        Parameters
        ----------
        newOutput: [pathlib.Path, str]
            The new output directory. Automattically converted into a path object
        """
        if (isinstance(newOutput, pathlib.PurePath)):
            #If the user gave a path as input
            if (not newOutput.exists()):
                raise ValueError("The new Output dir does not exist")
            if (newOutput.is_dir()):
                self.__outputPath = newOutput
            else:
                raise ValueError("The source path needs to lead to a directory")
        elif (isinstance(newOutput, str)):
            #If the user gave a string path
            newOutput = pathlib.Path(newOutput)
            self.setOutPath(newOutput)
        else:
            raise TypeError("Expected a string or path. Got {}".format(type(newOutput)))
        return None

    def setName(self, newName: str):
        """
        Sets the name of the experiment.

        Parameters
        ----------
        newName: str
            The string which represents the name of the experiment. This literally can be anything
        """
        assert isinstance(newName, str), "The new name needs to be a string. Got {}".format(type(newName))

        self.__name = newName
        return None

    def setMetaInfo(self, newMeta: List[str]):
        """
        Sets the meta data list of the experiment

        Parameters
        ----------
        newMeta: list(str)
            A list of strings representing any metadata lifted from the sourcefile
        """
        assert isinstance(newMeta, list) or isinstance(newMeta, tuple), "The new name needs to be a list of strings. Got {}".format(type(newMeta))

        for index in range(len(newMeta)):
            assert isinstance(newMeta[index], str), "All entries into the meta list need to be strings. Index {} was not instead was {}".format(index, type(newMeta[index]))

        self.__metaInfo = newMeta
        return None

    #<---------------------Getters--------------------->
    
    @property
    def plotConfig(self):
        """The plot configurator for the experiment"""
        return self.getPlotConf()

    def getPlotConf(self) -> plotConf:
        """Returns the plot configurator for the experiment"""
        return self.__plotConf

    @property
    def data(self):
        """The data of the experiment"""
        return self.getData()

    def getData(self) -> pd.DataFrame:
        """Returns the data of the experiment"""
        return self.__data

    @property
    def sourceFile(self):
        """The source file for the experiment"""
        return self.getSource()

    def getSource(self) -> pathlib.Path:
        """Returns the source of the experiment"""
        return self.__sourceFile

    @property
    def outputPath(self):
        """The output path of the experiment"""
        return self.getOutPath()

    def getOutPath(self) -> pathlib.Path:
        """Returns the output path of the experiment"""
        return self.__outputPath

    @property
    def name(self):
        """The name of the experiment"""
        return self.getName()

    def getName(self) -> str:
        """Returns the name of the experiment"""
        return self.__name

    @property
    def metaInfo(self):
        """The metadata of the experiment"""
        return self.getMeta()

    def getMeta(self) -> str:
        """Returns the metadata of the experiment"""
        return self.__metaInfo

    def getFormat(self):
        """Returns the save format for the experiment"""
        return self.__saveFormat

    #<---------------------Conditions--------------------->

    def isLoaded(self):
        """
        Indicates if the data for the experiment has been loaded in or not
        """
        if self.getData() is None:
            return False
        else:
            return True

    #<---------------------Generators--------------------->

    def readFile(self, delim: str = ",", begin_line: str = None, convert_dict = None, col_names = None):
        """
        Reads the source file to get the data into the experiment object. Needs the user to tell it how to read

        Parameters
        ----------
        delim: str
            The delimiter used to process the csv like values

        begin_line: str
            The final line before the csv like data

        convert_dict: dict
            What types the reader should convert the data to after reading it in (these are pandas types)

        col_names: list(str)
            The names of the columns after the reader sets up after
        """
        assert isinstance(begin_line, str) or begin_line is None, "The beginning line needs to be a string"
    
        meta_list = []

        if begin_line is None:
            pandas_read = pd.read_csv(self.getSource(), sep = delim, names = col_names, dtype = convert_dict)
        else:
            begin_line_met = False

            with open(self.getSource(), "r") as active_file:
                for line in active_file:
                    if begin_line_met:
                        pandas_read = pd.read_csv(active_file, sep = delim, names = col_names, dtype = convert_dict)
                        break
                    else:
                        meta_list.append(line)

                    if line == begin_line:
                        begin_line_met = True
        self.setMetaInfo(meta_list)
        self.setData(pandas_read)
        return None

    def nameParse(self) -> parse.Result:
        """
        Parses the name of the file into a series dictionary which is then used to construct the generated legend
        """
        parse_strings = [
            "{Type}_{Sample}_{Hour}-{Minute}-{Second}-{Msec}.{file_type}",
            "{Type}_{Sample}_{Background}_{Hour}-{Minute}-{Second}-{Msec}.{file_type}",
            "{Type}_{Sample}_{Background}_{Type2}_{Number}.{file_type}",
            "{Type}_{Sample}_{Type2}_{Number}.{file_type}"
        ]

        fileName = self.getSource().name

        for standard in parse_strings:
            result = parse.parse(standard, fileName)

            if result is not None:
                return result

        raise ValueError("The Input file name {} did not parse right".format(fileName))
        return None

    def outputNameGen(self) -> str:
        """
        Automatically generates the output name of the experiment using the source file and defined name
        """
        if self.getName() is None:
            return str.split(self.getSource().name, ".")[0] + self.getFormat()
        else:
            return self.getName() + "." + self.getFormat()

    def legendNameGen(self) -> str:
        """
        Automatically generates the legend name of the experiment using the source file and defined name
        """
        if self.getName() is None:
            parsedNames = self.nameParse()
            keys = parsedNames.named.keys()

            legendName = "" + parsedNames["Sample"]

            if "Background" in keys:
                legendName += " | BK: " + parsedNames["Background"]
            
            return legendName
        else:
            return self.getName()

    #<---------------------Plot Ops--------------------->

    @dispatch(namespace = __SpectExp_namespace)
    def plot(self) -> mplAx.Axes:
        """
        Plots the experiment by creating a new figure. Returns the axes which the data is plotted on. Automattically clears the current figure
        """
        plt.clf()
        fig, ax = plt.subplot(1)
        return self.plot(ax)

    @dispatch(mplAx.Axes, namespace = __SpectExp_namespace)
    def plot(self, ax: mplAx.Axes) -> mplAx.Axes:
        """
        Plots the experiment given a specific matplotlib axes. Will change the style though
        """
        return self.plot(ax, self.getPlotConf())

    @dispatch(mplAx.Axes, (plotConf, type(None)), namespace = __SpectExp_namespace)
    def plot(self, ax: mplAx.Axes, config: plotConf) -> mplAx.Axes:
        """
        Plots the experiment given a temporary plot configurator

        Parameters
        ----------
        ax: matplotlib.axes.Axes
            The axes you want to plot on

        config: plotConf
            The temporary plot configurator. Can be none in which case the plot configurator will plot without stylization
        """
        if isinstance(config, plotConf):
            if config.style_sheet is not None:
                with plt.style.context(config.style_sheet):
                    self.__basePlot(ax, config)
            else:
                self.__basePlot(ax, config)
        elif config is None:
            ax.plot(self.getData()[self.getData().columns[0]], self.getData()[self.getData().columns[1]], label = self.legendNameGen())
        else:
            raise TypeError("The plot config was not None or of type plotConf")
        return ax

    @dispatch(mplAx.Axes, namespace = __SpectExp_namespace)
    def __basePlot(self, ax: mplAx.Axes) -> mplAx.Axes:
        """
        An internal plotting function which keeps all of the code organized and in one place
        """
        return self.__basePlot(ax, self.getPlotConf())

    @dispatch(mplAx.Axes, plotConf, namespace = __SpectExp_namespace)
    def __basePlot(self, ax: mplAx.Axes, config: plotConf) -> mplAx.Axes:
        """
        An internal plotting function which keeps things cleaner
        """
        config.preOps(ax)
        ax.plot(self.getData()[self.getData().columns[0]], self.getData()[self.getData().columns[1]], label = self.legendNameGen())
        ax.legend()
        config.postOps(ax)
        return ax

    def save(self):
        """
        Saves the experiment to the output directory with the given saved format. Super useful to get an idea of what is going on
        """
        fig = plt.gcf()
        fig.clf()
        ax = plt.subplot(111)
        self.plot(ax)
        fig.savefig(self.getOutPath() / self.outputNameGen())
        return None

    #<---------------------Operations--------------------->

    def __str__(self):
        """A conversion / print method for the spectral experiment object"""
        main_str = ""

        #Name
        if self.getName() is not None:
            main_str += "Name: {}\n".format(self.getName())

        #Source file
        if self.getSource() is not None:
            main_str += "Sourcefile: {}\n".format(self.getSource().resolve())
        else:
            main_str += "Sourcefile: None\n"

        #Data
        if self.getData() is not None:
            main_str += "Data Shape: ({}, {})\n".format(*self.getData().shape)
        else:
            main_str += "Data Shape: Data not loaded\n"

        #Outpath
        if self.getOutPath() is not None:
            main_str += "Output Path: {}\n".format(self.getOutPath())
        else:
            main_str += "Output Path: None\n"

        return main_str

class SpectGroup:
    """
    A class which collects spectral experiments to make them collectively easier to handle

    Attributes
    ----------
    expList: list(SpectExp)
        A list of spectral experiments that are this group of experiments

    plotConf: plotConf
        The plot configurator used for this experimental group

    data: pandas.Dataframe
        The combined data of all of the experiments. Will only be directly accessible after doing sometype of operation. Can be checked if composed using isComposed()

    stats: pandas.Dataframe
        The general statistics of all of the composed experiments

    outputPath: pathlib.Path
        The output path for this experiment group. Where the files are saved

    name: str
        The overall name of this experiment group. Mainly affects the save name

    Methods
    -------
    plot(mode: str, ax: matplotlib.axes.Axes, config: plotConf) -> matplotlib.axes.Axes

    genSubgroup(self, expIndexes: list(int)) -> SpectGroup

    isComposed() -> Bool

    Compose()

    save(mode: str)
    """

    __SpectGroup_namespace = dict()

    #<---------------------Constructors--------------------->
    @dispatch(namespace = __SpectGroup_namespace)
    def __init__(self):
        """
        Default constructor for the Spectral Group
        """
        self.__expList = []
        self.__plotConf = plotConf()
        self.__data = None
        self.__stats = None
        self.__outPath = None
        self.__name = None

    @dispatch(list, plotConf, (pathlib.Path, str), str, namespace = __SpectGroup_namespace)
    def __init__(self, expList: List[SpectExp], config: plotConf, outputPath: pathlib.Path, name: str):
        """
        Builds the experiment group out of a list of spectral experiments. This is the root constructor

        Parameters
        ----------
        expList: list(SpectExp)
            The list of spectral experiments which the group is made out of

        config: plotConf
            The plot configurator used for the entire expreimental group

        outputPath: pathlib.Path
            The output path for the experiment group where the plots are saved

        name: str
            The name of the experiment
        """
        self.__init__()
        self.setExpList(expList)
        self.setPlotConf(config)
        self.setOutPath(outputPath)
        self.setName(name)

    @dispatch(list, dict, list, plotConf, (pathlib.Path, str), str, namespace = __SpectGroup_namespace)
    def __init__(self, fileList: List[str], readDict: dict, nameList: List[str], config: plotConf, outputPath: pathlib.Path, name: str):
        """
        Builds the experiment from a file list, read dictionary, and name list. Useful for building the experiment group when the experiments aren't previously designed

        Parameters
        ----------
        fileList: list(str)
            A list of files paths to use to create the experiments

        readDict: dict
            A special dictionary which defines how the experiment class reads in all of the experiments. Follows the "readFile" input structure in the SpectExp class in other words
                "delim": The delimiter for the csv style of the file, 
                "begin_line": The line on which the csv style data starts, 
                "convert_dict": what pandas types each column needs to be converted to, 
                "col_names": The names of the columns the first is always expected to be the wavelength

        nameList: list(str)
            A list of names to use for the experiments. Must be the same length as the number of experiments

        config: plotConf
            The plot configurator for the experiment group

        outputPath: pathlib.Path
            The dir where all of the output plots will be saved to

        name: str
            The name of the experiment group
        """
        self.__init__()
        assert len(fileList) == len(nameList), "The number of names must be equal to the number of experiments"

        tmp_exp = []

        for index in range(len(fileList)):
            tmp_exp.append(SpectExp(config, fileList[index], outputPath, nameList[index], readDict))

        self.__init__(tmp_exp, config, outputPath, name)

    @dispatch((pathlib.Path, str), plotConf, (pathlib.Path, str), str, namespace = __SpectGroup_namespace)
    def __init__(self, jsonFileList: pathlib.Path, config: plotConf, outputPath: pathlib.Path, name: str):
        """
        Builds the experimental group from a previously defined JSON file. Useful for quickly building previously used experiments and using things in a terminal

        Parameters
        ----------
        jsonFileList: pathlib.Path
            The JSON file to be used in constructing the experiment group. Each JSON file is expected to have a read dictionary inside it labeled with "readDict"

        config: plotConf
            The plot configurator for the experiment group

        outputPath: pathlib.Path
            The dir where all of the output plots will be saved to

        name: str
            The name of the experiment group
        """
        #Input Checks
        if (isinstance(jsonFileList, str)):
            jsonFileList = pathlib.Path(jsonFileList)
        assert jsonFileList.exists(), ValueError("The JSON file did not exist")
        assert jsonFileList.is_file(), ValueError("The JSON file was not a file")

        assert isinstance(config, plotConf), TypeError("The configurator was not of type plotConf")

        if (isinstance(outputPath, str)):
            outputPath = pathlib.Path(outputPath)
        assert outputPath.exists(), ValueError("The output path did not exist")
        assert outputPath.is_dir(), ValueError("The output path was not a directory")

        assert isinstance(name, str), TypeError("The group name needs to be a string")

        #Reading and checking the data
        with open(jsonFileList, "r") as file:
            jsonDict = json.load(file)

        assert isinstance(jsonDict, dict), TypeError("After reading the JSON object was not an object. Instead got {}. Make sure it's between curly braces".format(type(jsonDict)))
        #assert ("readDict" in jsonDict.keys()), ValueError("The JSON file did not define a read dictionary for the experiments")

        #Building all of the experiments
        expList = []

        if ("readDict" in jsonDict.keys()):
            for key in [x for x in jsonDict.keys() if x != "readDict"]:
                assert ("sourceFile" in jsonDict[key].keys()), KeyError("The sourceFile key was not defined in the {} experiment".format(key))
                assert ("outputPath" in jsonDict[key].keys()), KeyError("The outputPath key was not defined in the {} experiment".format(key))
                assert ("name" in jsonDict[key].keys()), KeyError("The name key was not defined in the {} experiment".format(key))

                if ("range" in jsonDict[key].keys()):
                    if len(jsonDict[key]["range"]) == 3:
                        for num in range(jsonDict[key]["range"][0], jsonDict[key]["range"][1] + 1, jsonDict[key]["range"][2]):
                            expList.append(SpectExp(config, jsonDict[key]["sourceFile"].format(num), jsonDict[key]["outputPath"].format(num), jsonDict[key]["name"].format(num), jsonDict["readDict"]))
                    elif len(jsonDict[key]["range"]) == 2:
                        for num in range(jsonDict[key]["range"][0], jsonDict[key]["range"][1] + 1):
                            expList.append(SpectExp(config, jsonDict[key]["sourceFile"].format(num), jsonDict[key]["outputPath"].format(num), jsonDict[key]["name"].format(num), jsonDict["readDict"]))
                    else:
                        raise ValueError("The range was not defined correctly")
                else:
                    expList.append(SpectExp(config, jsonDict[key]["sourceFile"], jsonDict[key]["outputPath"], jsonDict[key]["name"], jsonDict["readDict"]))
        else:
            for key in [x for x in jsonDict.keys() if x != "readDict"]:
                assert ("sourceFile" in jsonDict[key].keys()), KeyError("The sourceFile key was not defined in the {} experiment".format(key))
                assert ("outputPath" in jsonDict[key].keys()), KeyError("The outputPath key was not defined in the {} experiment".format(key))
                assert ("name" in jsonDict[key].keys()), KeyError("The name key was not defined in the {} experiment".format(key))

                if ("range" in jsonDict[key].keys()):
                    if len(jsonDict[key]["range"]) == 3:
                        for num in range(jsonDict[key]["range"][0], jsonDict[key]["range"][1] + 1, jsonDict[key]["range"][2]):
                            expList.append(SpectExp(config, jsonDict[key]["sourceFile"].format(num), jsonDict[key]["outputPath"].format(num), jsonDict[key]["name"].format(num)))
                    elif len(jsonDict[key]["range"]) == 2:
                        for num in range(jsonDict[key]["range"][0], jsonDict[key]["range"][1] + 1):
                            expList.append(SpectExp(config, jsonDict[key]["sourceFile"].format(num), jsonDict[key]["outputPath"].format(num), jsonDict[key]["name"].format(num)))
                    else:
                        raise ValueError("The range was not defined correctly")
                else:
                    expList.append(SpectExp(config, jsonDict[key]["sourceFile"], jsonDict[key]["outputPath"], jsonDict[key]["name"]))

        self.__init__(expList, config, outputPath, name)

    #<-----------------------Setters------------------------>
    def setExpList(self, expList: List[SpectExp]):
        """
        Sets the list of experiments to be used by the experimental group

        expList: list(SpectExp)
            A list of experiments used by the group
        """
        for index in range(len(expList)):
            if (not isinstance(expList[index], SpectExp)):
                raise TypeError("Each experiment in the new spectral experiments needs to be of type SpectExp. Got {} at index{}".format(type(expList[index]), index))
        self.__expList = expList
        self.__data = None
        self.__stats = None
        return None

    def addExp(self, exp: SpectExp):
        """
        Adds an experiment to the list of experiments for the group

        exp: SpectExp
            The experiment which will be added to the group
        """
        assert isinstance(exp, SpectExp), "Expected a spectral experiment but got {}".format(type(exp))

        self.__expList.append(exp)
        self.__data = None
        self.__stats = None
        return None

    def setPlotConf(self, config: plotConf):
        """
        Sets the plot configurator for this experiment group. Effectively this stylizes the plot

        Parameters
        ----------
        newConf: plotConf
            The new plot configurator to be set
        """
        assert isinstance(config, plotConf), "The new plot configurator needs to be a plot configurator. Got {}".format(type(config))

        self.__plotConf = config
        return None

    def setData(self, newData: pd.DataFrame):
        """
        Sets the data associated with the experimental group and checks to make sure that it's alright

        newData: pandas.DataFrame
            A pandas dataframe which describes the data for the experiment group. Usually auto generated by the group. Must have a wavelength column
        """
        assert isinstance(newData, pd.DataFrame), "The new data needs to be a pandas dataframe"
        assert "Wavelength" in newData.columns, "The new data needs to have a wavelength column"
        self.__data = newData
        return None

    def setStats(self, newStats: pd.DataFrame):
        """
        Sets the statistics dataframe of the experiment group. Not really intended to be used by the user

        newStats: pandas.DataFrame
            The new statistics to be used by the experiment group
        """
        assert isinstance(newStats, pd.DataFrame), "The new data needs to be a pandas dataframe"
        self.__stats = newStats
        return None

    def setOutPath(self, newOutput: pathlib.Path):
        """
        Sets the output path of the experiment group

        Parameters
        ----------
        newOutput: [pathlib.Path, str]
            The new output directory. Automattically converted into a path object
        """
        if (isinstance(newOutput, pathlib.PurePath)):
            #If the user gave a path as input
            if (not newOutput.exists()):
                raise ValueError("The new Output dir does not exist")
            if (newOutput.is_dir()):
                self.__outPath = newOutput
            else:
                raise ValueError("The source path needs to lead to a directory")
        elif (isinstance(newOutput, str)):
            #If the user gave a string path
            newOutput = pathlib.Path(newOutput)
            self.setOutPath(newOutput)
        else:
            raise TypeError("Expected a string or path. Got {}".format(type(newOutput)))
        return None

    def setName(self, newName: str):
        """
        Sets the name of the experiment group.

        Parameters
        ----------
        newName: str
            The string which represents the name of the experiment. This literally can be anything
        """
        assert isinstance(newName, str), "The new name needs to be a string. Got {}".format(type(newName))

        self.__name = newName
        return None

    #<-----------------------Getters------------------------>
    @dispatch(namespace = __SpectGroup_namespace)
    def getExpList(self) -> List[SpectExp]:
        """Returns the experiment list"""
        return self.__expList

    @dispatch(list, namespace = __SpectGroup_namespace)
    def getExpList(self, colNums: List[int]):
        return_list = []
        for index in range(len(colNums)):
            assert isinstance(colNums[index], int), "All indexes must be integers. Got {} at index {}".format(type(colNums[index]), index)
            assert colNums[index] < len(self.__expList), "All indexes must be within range. Index {} was out of range".format(index)
            return_list.append(self.__expList[colNums[index]])

        return return_list

    def getExp(self, index: int) -> SpectExp:
        """Returns a specific experiment of the experiment list"""
        return self.__expList[index]

    def getPlotConf(self) -> plotConf:
        """Returns the plot configurator for the experiment group"""
        return self.__plotConf

    def getData(self) -> pd.DataFrame:
        """Returns the data for the experiment group"""
        return self.__data

    def getStats(self) -> pd.DataFrame:
        """Returns the statistics dataframe for the experiment group"""
        return self.__stats

    def getOutPath(self) -> pathlib.Path:
        """Returns the output path for the experiment group"""
        return self.__outPath

    def getName(self) -> str:
        """Returns the name of the experiment group"""
        return self.__name

    #<----------------------Conditions---------------------->
    def isComposed(self) -> bool:
        """A conditional formula to check if the data has all of the experiments loaded in properly"""
        if self.getData() is None:
            return False
        else:
            return True

    def isStats(self) -> bool:
        """A conditional formula to check if the statistics have been calculated yet"""
        if self.getStats() is None:
            return False
        else:
            return True

    #<----------------------Generators---------------------->
    def genSubgroup(self, groupDef: List[List[int]]) -> 'SpectGroup':
        """
        This generates an experimental subgroup given a list of indicies. Useful if you find that the experiment group has sub patterns

        Parameters
        ----------
        groupDef: list(list(int))
            This is a list of a list of integers where the integers represent indicies in the experiment list
        """
        Subgroup = []

        for main_index in range(len(groupDef)):
            for second_index in range(len(groupDef[main_index])):
                assert isinstance(groupDef[main_index][second_index], int), "The subgroup definition can only have integer indecies"
            Subgroup.append(SpectGroup(self.__expList[groupDef[main_index]], self.getPlotConf(), self.getOutPath(), "Subgroup #{} of {}".format(main_index + 1, self.getName())))
        return Subgroup

    def genStats(self):
        """Generates the statistics dataframe from the data of the experimental group. Currently calculates the min, max, mean, and std of each row"""
        if not self.isComposed():
            self.Compose()
        
        tmp_stats = self.getData()[["Wavelength"]].copy()
        tmp_stats["min"] = self.getData().drop("Wavelength", axis = 1).min(axis = 1)
        tmp_stats["max"] = self.getData().drop("Wavelength", axis = 1).max(axis = 1)
        tmp_stats["mean"] = self.getData().drop("Wavelength", axis = 1).mean(axis = 1)
        tmp_stats["std"] = self.getData().drop("Wavelength", axis = 1).std(axis = 1)
        self.setStats(tmp_stats)
        return None

    #<-----------------------Plot Ops----------------------->
    @dispatch(str, mplAx.Axes, (plotConf, type(None)), namespace = __SpectGroup_namespace)
    def plot(self, mode: str, ax: mplAx.Axes, config: plotConf) -> mplAx.Axes:
        """
        Plots the experimental group data in a specific way on the given axes

        Parameters
        ----------
        mode: str
            A string representing the plotting mode of the experimental group. The valid options are the following
                stack: Plots all of the experimental group onto the same set of axes
                range: Plots the minimum and maximum of the data ranges. Gives a good idea of the possible values
                1std: Plots the average and the first standard deviation from the average. Gives an idea of the error

        ax: matplotlib.axes.Axes
            The axes onto which the plot will be made

        config: plotConf
            The configurator used to style the plot. Can be None to have no stylization on the plot
        """
        if isinstance(config, plotConf):
            if config.style_sheet is not None:
                with plt.style.context(config.style_sheet):
                    config.preOps(ax)
                    self.__plotSwitch(mode, ax)
                    config.postOps(ax)
            else:
                config.preOps(ax)
                self.__plotSwitch(mode, ax)
                config.postOps(ax)
        elif config is None:
            self.__plotSwitch(mode, ax)
        else:
            raise TypeError("The plot config was not None or of type plotConf")
        ax.legend()
        return ax

    @dispatch(str, mplAx.Axes, namespace = __SpectGroup_namespace)
    def plot(self, mode: str, ax: mplAx.Axes) -> mplAx.Axes:
        """
        Plots all of the experimental groups data on the given axes using the experimental groups default configurator

        Parameters
        ----------
        mode: str
            A string representing the plotting mode of the experimental group. The valid options are the following
                stack: Plots all of the experimental group onto the same set of axes
                range: Plots the minimum and maximum of the data ranges. Gives a good idea of the possible values
                1std: Plots the average and the first standard deviation from the average. Gives an idea of the error

        ax: matplotlib.axes.Axes
            The axes onto which the plot will be made
        """
        return self.plot(mode, ax, self.getPlotConf())

    @dispatch(list, str, mplAx.Axes, (plotConf, type(None)))
    def plot(self, gList: list, mode: str, ax: mplAx.Axes, config: plotConf) -> mplAx.Axes:
        """
        Plots the Spectral group given a list of other spectral groups. Plots using the same plotConf and mode

        Parameters
        ----------
        gList: List(SpectGroup)
            The spectral group list which tells which groups to plot on the same plot

        mode: str
            A string representing the plotting mode of the experimental group. The valid options are the following
                stack: Plots all of the experimental group onto the same set of axes
                range: Plots the minimum and maximum of the data ranges. Gives a good idea of the possible values
                1std: Plots the average and the first standard deviation from the average. Gives an idea of the error

        ax: matplotlib.axes.Axes
            The axes to plot all of the groups onto

        config: plotConf
            The configurator to use when plotting
        """
        if isinstance(config, plotConf):
            if config.style_sheet is not None:
                with plt.style.context(config.style_sheet):
                    config.preOps(ax)
                    self.__plotSwitch(mode, ax)

                    #Iterate over list
                    for index in range(len(gList)):
                        assert isinstance(gList[index], SpectGroup), "Index {} of the spectral group list was not a spectral group".format(index)
                        gList[index].plot(mode, ax, None)
                    config.postOps(ax)
            else:
                config.preOps(ax)
                self.__plotSwitch(mode, ax)

                #Iterate over list
                for index in range(len(gList)):
                    assert isinstance(gList[index], SpectGroup), "Index {} of the spectral group list was not a spectral group".format(index)
                    gList[index].plot(mode, ax, None)
                config.postOps(ax)
        elif config is None:
            self.__plotSwitch(mode, ax)

            #Iterate over list
            for index in range(len(gList)):
                assert isinstance(gList[index], SpectGroup), "Index {} of the spectral group list was not a spectral group".format(index)
                gList[index].plot(mode, ax, None)
        else:
            raise TypeError("The plot config was not None or of type plotConf")
        ax.legend()
        return ax

    @dispatch(list, str, mplAx.Axes)
    def plot(self, gList: list, mode: str, ax: mplAx.Axes) -> mplAx.Axes:
        """
        Plots the Spectral group given a list of other spectral groups. Plots using the SpectGroup's default plot configurator

        Parameters
        ----------
        gList: List(SpectGroup)
            The spectral group list which tells which groups to plot on the same plot

        mode: str
            A string representing the plotting mode of the experimental group. The valid options are the following
                stack: Plots all of the experimental group onto the same set of axes
                range: Plots the minimum and maximum of the data ranges. Gives a good idea of the possible values
                1std: Plots the average and the first standard deviation from the average. Gives an idea of the error

        ax: matplotlib.axes.Axes
            The axes to plot all of the groups onto
        """
        return self.plot(gList, mode, ax, self.getPlotConf())

    def __plotSwitch(self, mode: str, ax: mplAx.Axes) -> mplAx.Axes:
        """
        An internal function which determines the different possible plotting modes for the experimental group

        Parameters
        ----------
        mode: str
            The parameter used as a switch to indicate which mode to use

        ax: matplotlib.axes.Axes
            The axes onto which the data will be plotted
        """
        if mode.lower() == "stack":
            for exp in self.getExpList():
                exp.plot(ax, None)
        elif mode.lower() == "range":
            if not self.isStats():
                self.genStats()
            ax.fill_between(self.getStats()["Wavelength"], self.getStats()["min"], self.getStats()["max"], label = self.getName() + " RANGE")
        elif mode.lower() == "1std":
            if not self.isStats():
                self.genStats()

            ax.fill_between(self.getStats()["Wavelength"], self.getStats()["mean"] - self.getStats()["std"], self.getStats()["mean"] + self.getStats()["std"], alpha = 0.2)
            ax.plot(self.getStats()["Wavelength"], self.getStats()["mean"], label = self.getName() + " AVG")
        else:
            raise ValueError("The input mode was incorrect. Got {}".format(mode))
        return ax

    @dispatch(list, str, str)
    def save(self, gList: list, mode: str, fileName: str):
        """
        Saves the experimental group into the output location using the given mode and file name

        Parameters
        ----------
        mode: str
            A string representing the plotting mode of the experimental group. The valid options are the following
                stack: Plots all of the experimental group onto the same set of axes
                range: Plots the minimum and maximum of the data ranges. Gives a good idea of the possible values
                1std: Plots the average and the first standard deviation from the average. Gives an idea of the error

        fileName: str
            The name under which you want to save the file

        gList: List(SpectGroup)
            The list of spectral groups you want to save on the same file given a mode
        """
        fig = plt.gcf()
        fig.clf()
        ax = plt.subplot()
        self.plot(gList, mode, ax)
        fig.savefig(self.getOutPath() / (fileName + ".png"))
        return None

    @dispatch(list, str)
    def save(self, gList: list, mode: str):
        """
        Saves the experimental group into the output location using the given mode and file name

        Parameters
        ----------
        mode: str
            A string representing the plotting mode of the experimental group. The valid options are the following
                stack: Plots all of the experimental group onto the same set of axes
                range: Plots the minimum and maximum of the data ranges. Gives a good idea of the possible values
                1std: Plots the average and the first standard deviation from the average. Gives an idea of the error

        gList: List(SpectGroup)
            The list of spectral groups you want to save on the same file given a mode
        """
        fig = plt.gcf()
        fig.clf()
        ax = plt.subplot()
        self.plot(gList, mode, ax)
        fig.savefig(self.getOutPath() / (self.getName() + ".png"))
        return None

    @dispatch(str, str)
    def save(self, mode: str, fileName: str):
        """
        Saves the experimental group into the output location using the given mode and file name

        Parameters
        ----------
        mode: str
            A string representing the plotting mode of the experimental group. The valid options are the following
                stack: Plots all of the experimental group onto the same set of axes
                range: Plots the minimum and maximum of the data ranges. Gives a good idea of the possible values
                1std: Plots the average and the first standard deviation from the average. Gives an idea of the error

        fileName: str
            The name under which you want to save the file
        """
        fig = plt.gcf()
        fig.clf()
        ax = plt.subplot()
        self.plot(mode, ax)
        fig.savefig(self.getOutPath() / (fileName + ".png"))
        return None

    @dispatch(str)
    def save(self, mode: str):
        """
        Saves the experimental group into the output location using the given mode

        Parameters
        ----------
        mode: str
            A string representing the plotting mode of the experimental group. The valid options are the following
                stack: Plots all of the experimental group onto the same set of axes
                range: Plots the minimum and maximum of the data ranges. Gives a good idea of the possible values
                1std: Plots the average and the first standard deviation from the average. Gives an idea of the error
        """
        self.save(mode, self.getName())
        return None

    #<----------------------Operations---------------------->
    def __Compose(self, colIndexes: List[int]):
        """
        An internal version of the compose function which is a bit more powerful. Making it internal makes things easier to work with externally but also makes it easy to maintain

        Parameters
        ----------
        colIndexes: list(int)
            A list of integers telling the group which experiments to compile into the data dataframe
        """
        for index in colIndexes:
            if not self.getExp(index).isLoaded():
                raise ValueError("Experiment at index {} was not loaded".format(index))
        tmp_data = reduce(lambda x, y: pd.merge(x, y, on = ["Wavelength"], suffixes = ("_", "_")), [x.getData() for x in self.getExpList()]) #TODO: Implement getExpList properly
        tmp_data.columns = ["Wavelength"] + ["Exp_{}".format(x) for x in colIndexes]
        self.setData(tmp_data)
        return None

    def Compose(self):
        """
        Takes all of the data from the experiment list and composes it into the data of the experiment group. This makes things easier to manage
        """
        self.__Compose([*range(0, len(self.getExpList()))])
        return None
