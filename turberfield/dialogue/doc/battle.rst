..  Titling
    ##++::==~~--''``

Example 1: Battle Royal
:::::::::::::::::::::::

Turberfield comes with a couple of examples. We will start with the simplest.
What we learn here will set us up for the more advanced example later.

This is our first encounter with the Turberfield rehearsal tool. We will use
it to preview the action in the first example.

.. admonition:: What are my options?

    It may be that this is the first time you have launched a Python program from
    your computer's command line. If so, there's a couple of things to understand
    first.

    When you launch a command line program, you do so by typing its name. You then
    follow that with *options* which are extra instructions to control the way the
    program behaves.

    The Turberfield rehearsal tool takes several options; typing them all out every
    time is an annoyance. So the essential ones are stored in a text file called
    *rehearse.cli*. You can pass this file to the program instead and it will take
    the options from there. You can add more from the command line at the same time
    by typing them afterwards in the usual way.

    To launch the rehearsal tool with stored options, precede the path to the options
    file with a '`@`' symbol, eg:

Rehearsal
=========

On Linux or MacOSX::

    $ ~/py3.5/bin/turberfield-rehearse @turberfield/dialogue/sequences/battle/rehearse.cli

On Windows 8.1::

    > start %USERPROFILE%\py3.6\Scripts\turberfield-rehearse @turberfield/dialogue/sequences/battle/rehearse.cli

From now on, I'll assume you know how to operate the command line on your computer.
Further instructions will give the Linux form of commands only, and omit the prompt
character.

Here's what you should see in your terminal window, including a sound effect at the
appropriate point::

    Combat


        Action


          Scratchy
                  I hate the way you use me,  Itchy  !

          Ol' Rusty Chopper
                  **Whack!**

          Itchy
                  Uuurrggh!

        Itchy.state = 0

This is a short scene in a fictional cartoon. In order to produce this for
an audience, we bring two components together:

* An ensemble_ of Actors
* A folder_ of Dialogue

.... admonition:: All the world's a stage

.. admonition:: All the world's a stage

   Explain every object has a voice. Named objects are Personae

Ensemble
========

This is where the actors live.
Terminology - Personae vs actors, characters.

* class inheritance
* Persona - name
* Stateful - state
* Assembly - use to mention --web in passing
* integer state used for alive/dead

Folder
======

Defines the script files

* :roles:
* Launch again with repeat=1

::

    Combat


        Action


          Scratchy
                  I hate the way you use me,  Itchy  !

          Ol' Rusty Chopper
                  **Whack!**

          Itchy
                  Uuurrggh!

        Itchy.state = 0

          Ol' Rusty Chopper
                  I hate the way you use me,  Scratchy  !

          Ol' Rusty Chopper
                  **Whack!**

          Scratchy
                  Uuurrggh!

        Scratchy.state = 0

    Press return.
