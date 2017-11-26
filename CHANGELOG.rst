..  Titling
    ##++::==~~--''``

.. This is a reStructuredText file.

Change Log
::::::::::

0.13.0
======

* DataObject `id` attribute is now a `uuid.UUID` object.

0.12.0
======

* Refactored the `rehearse` function so it uses `Performer`. Its first argument is now
  documented as a sequence. Legacy behaviour is preserved.

0.11.0
======

* Field lists at the document level are available via the  `metadata` attribute of the model.
* Substitution references to Python values are properly resolved in the bodies of field lists.
* There is a new utility, `turberfield-dialogue` for producing a printable screenplay.
* The viewer module now registers all references with `turberfield.utils.assembly.Assembly`.
* The `Performer` class is now part of the public API.

0.10.1
======

* Changelog fixes.

0.10.0
======

* Substitution references are now permitted in the `resource` argument to
  an FX directive.

0.9.0
=====

* `Turberfield.dialogue.performer` and matching tests implement the new Performer
  class. This was first prototyped in the `bluemonday78` episode of Addison Arches.

0.8.0
=====

* `turberfield-rehearse` **--web** option works tolerably in Firefox.
* Added **strict** mode for casting a rehearsal.
* Interludes now see a sequence of folders they may **branch** to.
* State matching is hierarchical; '31' matches a criterion of '3'.
