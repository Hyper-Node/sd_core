# sd_core
Social data experiments core module 

### Description
Since the social data experiments project is the starting point for many other projects, a common 
ground of classes and functions was established. This project aims to provide a centralized version 
of those functions, which are integrated in other social data related projects. 


### Usage 

To add this module to another module: 
```
git submodule add https://github.com/Hyper-Node/sd_core.git
```
To update this module within another module:
```
git submodule update --init --recursive
```

The initialization of the main modules in files looks similar like this, it is required to initialize the config and conditional
print before using the most other classes in sd_core:
```
from sd_core.configuration_handler import ConfigurationHandler
from sd_core.conditional_print import ConditionalPrint
from sd_core.text_file_loader import TextFileLoader

CODED_CONFIGURATION_PATH = './configurations/my_config.conf'
config_handler = ConfigurationHandler(first_init=True, fill_unkown_args=True,\
                                      coded_configuration_paths=[CODED_CONFIGURATION_PATH])
config = config_handler.get_config()
cpr = ConditionalPrint(config.PRINT_MAIN, config.PRINT_EXCEPTION_LEVEL, config.PRINT_WARNING_LEVEL,
                       leading_tag="main")
                      
                      
# text_file_loader (initializing config handler is required for using the other modules) 
text_file_loader = TextFileLoader()
```
The base configuration file should at least have the following entries. An example configuration file is
provided as 'example_conf.conf' in the root of sd_core.
```
PRINT_MAIN = true
PRINT_EXCEPTION_LEVEL = true
PRINT_WARNING_LEVEL = true
PRINT_TXT_FILE_LOADER = true
PRINT_GOOGLE_CLIENT = true
```