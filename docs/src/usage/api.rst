API Usage
=========

External systems might like to interact with Ghiro and share data with it.
For example you might be intrested in integrating Ghiro with your analysis environment or
your scripts; for example you would have a system sending images to Ghiro and a script to
fetch analysis results and process them.
Ghiro comes with a set of JSON API to help automation and integration with external systems.
All major functionalities are accessible through API, although API will be expanded and
enriched in future releases.
The available API methods are:

    * Create a new case
    * Image upload for analysis (create a new analysis)

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