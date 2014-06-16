API Usage
=========

External systems might like to interact with Ghiro and share data with it.
For example you might integrate Ghiro with your analysis environment, have a system
sending images to Ghiro and fetch results.
Ghiro comes with a set of JSON API to help automation and integration with external systems.
All major funtionalities are accessible through API.

/api/cases/new
------------------

    **POST /api/cases/new**

        Adds a new case with naem, description optional. Returns the ID of the newly created case.

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