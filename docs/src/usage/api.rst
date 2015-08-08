API Usage
=========

External systems might like to interact with Ghiro, use their features and
share data with it.
For example you might be interested in integrating Ghiro with your analysis
environment or your scripts, to integrate Ghiro with your analysis pipeline.
For example you would have a system sending images to Ghiro and a script to
fetch analysis results and process them to send an email only if some
circumstances are met.
Ghiro comes with a set of JSON API to help automation and integration with
external systems.
All major functionalities are available through API, although API will be
expanded and enriched in future releases.

The available API methods are:

    * Create a new case
    * Show case contents
    * Image upload for analysis (create a new analysis)
    * Fetch report of an image analysis

You can use these API as follows.

/api/cases/new
--------------

    **POST /api/cases/new**

        Adds a new case with name, description optional. Returns the ID of the newly created case.

        **Example request**::

            curl -kis -F name=foo -F description=bar -F api_key=YOUR_API_KEY http://127.0.0.1:8000/api/cases/new

        **Example response**::

            {"id": 6}

        **Form parameters**:
            * ``name`` *(required)* - case name
            * ``api_key`` *(required)* - your API key (get it in your profile page)
            * ``description`` *(optional)* - case description

        **Status codes**:
            * ``200`` - success
            * ``400`` - failure (see the message for error description)

/api/cases/show
---------------

    **POST /api/cases/show**

        Shows a case. Including image ids for this case.

        **Example request (requesting case with ID 3)**::

            curl -kis -F case_id=3 -F api_key=YOUR_API_KEY http://127.0.0.1:8000/api/cases/show

        **Example response**::

            {"status": "O", "images": [2, 1], "description": "Test case.", "id": 3, "name": "Test"}

        **Form parameters**:
            * ``case_id`` *(required)* - case ID
            * ``api_key`` *(required)* - your API key (get it in your profile page)

        **Status codes**:
            * ``200`` - success
            * ``400`` - failure (see the message for error description)

/api/images/new
---------------

    **POST /api/images/new**

        Adds a new image and enqueue it for analysis. Returns the ID of the newly created analysis.
        This is an example, you should put your Ghiro's server IP address and port in the url.

        **Example request (image not added to a case)**::

            curl -kis -F image=@path_to_image.jpg -F api_key=YOUR_API_KEY http://127.0.0.1:8000/api/images/new

        **Example request (image added to case ID 1)**::

            curl -kis -F case_id=1 -F image=@path_to_image.jpg -F api_key=YOUR_API_KEY http://127.0.0.1:8000/api/images/new

        **Example response**::

            {"id": 6}

        **Form parameters**:
            * ``case_id`` *(optional)* - case ID
            * ``image`` *(required)* - image file to upload for analysis
            * ``api_key`` *(required)* - your API key (get it in your profile page)

        **Status codes**:
            * ``200`` - success
            * ``400`` - failure (see the message for error description)

/api/images/report
------------------

    **POST /api/images/report**

        Get image analysis report.

        **Example request (requesting image analysis with ID 1)**::

            curl -kis -F task_id=1 -F api_key=YOUR_API_KEY http://127.0.0.1:8000/api/images/report

        **Example response of completed analysis (truncated)**::

            {"id": 1, "status": "C", "data": {"signatures": [], "hash": {"sha1\": "fda88a5aa ..snip..

        **Example response of not completed analysis (truncated)**::

            {"id": 1, "status": "P"}

        **Form parameters**:
            * ``task_id`` *(required)* - analysis id
            * ``api_key`` *(required)* - your API key (get it in your profile page)

        **Status codes**:
            * ``200`` - success
            * ``400`` - failure (see the message for error description)