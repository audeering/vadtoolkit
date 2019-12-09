VAD-Toolkit
===========

Converts `VAD Toolkit (vadtoolkit)` to the audata_ format and publishes it on Artifactory.

Prerequisites
-------------

Java_ must be installed.

Publishing
----------

Run `./gradlew publish`.

An Artifactory_ account with deploy permissions must be configured via Gradle properties `artifactoryUser` and `artifactoryApiKey`.

.. _audata: https://gitlab.audeering.com/tools/audata
.. _Artifactory: https://artifactory.audeering.com/
.. _Java: https://sdkman.io/sdks#java
