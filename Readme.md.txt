# Singular


**Singular is a very simple, but powerful, application to programatically call different functions on Cisco Collaboration products.**

Singular - Telepresence Endpoint Manager
========================================

? Introduction
---------------

This is perhaps the most popular feature among our customers. Simply input the endpoint credentials, the list of your TP endpoints you want to cover on the left panel,and the actions you want to run on the right panel. Click execute and each command will be processed top down on each Telepresence endpoint. Telepresence endpoint manager uses REST APIs on port 443,which makes the execution fast, secure and reliable. Since 1.2 release there is also an output panel to quickly view the results of ´show´ commands and execution result of other actions.


.. image:: https://live.staticflickr.com/65535/47068045594_d9801396dd_b.jpg


? Installation
--------------

The application is an executable that runs in memory. It does not install any file, DLL or registry in your PC or VM.

There is no software requirements prior to run Singular. Windows7, Windows10 and OSX are supported OS.

There is no need to have Administrator rights on the machine.


? Command Pannel
-----------------
Commands are executed sequentially for each IP address on the left panel. Available commands are custom functions that call, in the backend, REST APIs to get the job done.

Before the first command is executed, Singular asks the endpoint its status and stores different parameters like software type, version, URI, System Name and others. Thanks to these parameters, the same command works transparently on different endpoint software.

Lines  starting with # in this panel are ignored (considered comments).

To see the list of supported commands, please issue the command **help()**

user input values are expressed within <>, so you would execute *set configItem(<ip_address>)* as *set configItem(10.1.1.3)*

fixed option values are shown between /, so you would execute *set activeControl(auto/off) as *set configItem(auto)*

? Help commands
------------------------------

To list all supported commands

.. code:: python

    help()

? Configuration commands (set)
------------------------------

Supported on all software types.

**Configure TFTP addresses**

.. code:: python

    set externalManagerAddress(<ip address>)
    set externalManagerAlternateAddress(<ip address>)


**Set provisioning mode**  

Availables modes are:

    For TC software: Off, TMS, VCS, CallWay,CUCM, Auto, Edge
    
    For CE/roomOS software: Off, TMS, VCS, Webex, CUCM, Auto, Edge

.. code:: python

    set provisioningMode(<mode>)


**Other commands supported on all SW types** 

Supported on all software types. Available modes are: On/Off

.. code:: python

    set autoAnswer(on/off)
    set sipProxy1(<ip_address>)
    set sipProxy2(<ip_address>)
    set sipProxy3(<ip_address>)
    set sipProxy4(<ip_address>)


**Other CE/RoomOS only commands** 

.. code:: python

    set wakeupOnMotionDetection(on/off)
    set activeControl(auto/off)

? Delete commands
------------------

**Delete ITL** 

Supported on all software types except roomOS (cloud registered)

.. code:: python

    delete itl()

**Delete macro files** 

Supported on CE and roomOS

.. code:: python

    delete macro(<file_name>)
    
    
with the commands already seen you could migrate an endpoint between UCM clusters with the below sequence:

.. code:: python

    set provisioningMode(Off)
    delete itl()
    set externalManagerAddress(<ip address>)
    set externalManagerAlternateAddress(<ip address>)
    set provisioningMode(CUCM)
    
    

? Show commands
---------------------


**show status() and show config()** 

show status() and show config() can be issued with or without a filter. If no argument is passed, all status or configuration items of each device will be shown in the output pannel. Filters are case sensitive.

.. code:: python

    show status()
    show config()
    show status(version)
    show config(ActiveControl) 
    show status(Status.SIP.Registration.Status)
    show status(SIP.Proxy.Address)

? Upload commands
--------------------

Files need to be always located in the same path as Singular executable.

**Branding** 

Branding is only supported on CE/roomOS software endpoints.

.. code:: python

    upload brandingAwake(<image_file_name.ext>)
    upload brandingHalfwake(<image_file_name.ext>)
    upload brandingBackground(<image_file_name.ext>)
    
**Wallpaper**

Uploading Wallpapers is only supported on TC software.

.. code:: python

    upload wallpaper(<image_file_name.ext>)
    
**Macros and custom buttons**

Macros and custom buttons are supported only on CE and roomOS software.

Upload a macro file in macro editor. Note that the macro name will be taken from the file name (without the extension)

.. code:: python

    upload macro(<macro_example.js>)
    
? Enable commands
--------------------

To enable macro editor, which is disabled by default

.. code:: python

    enable macroEditor()
    enable macro(<macro_name)  <== This is the macro name and not macro file (there is no extension)
    
? Disable commands
--------------------

**Commands supported on CE/RoomOS SW**

.. code:: python

    disable macroEditor()
    disable macro(<macro_name>)  <== This is the macro name and not macro file (there is no extension)
    


? Miscellaneous commands
--------------------------

**Commands supported on all SW types**

.. code:: python

    factoryReset()
    restart()
    
