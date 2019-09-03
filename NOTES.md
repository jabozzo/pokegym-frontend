# Additional Notes

- Backend exposes a single url `.../last`, available through GET. Each time this url is called this list shifts one position if there are more pokemon to display. This is not consisten with a RESTful approach since GET methods are supposed to be read-only and this operation modifies the  underlying resource.

- From the frontend, only the url strings were changed.

- The file `backend/python/config.py` holds constants to change:
  - The host address and port.
  - The maximum amount of pokemon displayed at a given time.
  - A minimum amount of pokemon to display at a given time, after the list have this amount of pokemon displayed it stops shifting.
  - Whenever to cache the pokedex. Since it doesn't change for extended period of time, the pokedex can be queried once and the stored.
  - The directory `backend/arrival_examples` contains examples of arrival files.

## SECURITY NOTE

- Since `frontend/index.html` is opened from disk and the backend is hosted by localhost, `Access-Control-Allow-Origin` has been set to `*` to bypass the browser security policy.
