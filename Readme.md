Github navigator assignment task
--------------------------------

- In this file I do only present the background information on the task I was assigned. General information on the code is located in "Readme.md".

- I solved this task using flask, which is great for small web applications like this one.

- I have never used flask productively before, but i considered it a couple of times. I always ended up using django in these cases because the projects were planned to be somewhat bigger and more frontend-heavy. I find django allows for a more conventional code organization in such cases.

- I didn't spend a lot of time on optical polishing, but I think I met most specs (data formatting) given through the assignment, template and example.

- Coding went smoothly, and I had the app display commit details even before I hit githubs rate limit. I figured that that should be circumvented as well, so I added a way to provide optional OAUTH credentials to the app.

- Since I was working with github already, I could not resist the temptation to put the project on github (without any reference to you, or assignment texts). The repo can be found here: https://github.com/isnok/github-navigator

- If you request me to take it off from github, then I will do so promptly of course.

- File structure:
.
├── application.py    -- The uWSGI application
├── github_search.py  -- A program library that i created for API-communication with github
├── oauth.json        -- (optional) OAUTH credentials (you need to create that by yourself, see Readme.md)
├── Readme.md         -- The Project Readme. Consider this an extension of this document
├── requirement.txt   -- project dependencies, as by python-convention
└── templates         -- flask by default searches templates here. So I went with that.
    ├── index.html    -- Template for the additional index page of the application
    └── results.html  -- The template for the search results page

- The results template could be cleaned up a bit more, but I figured that that is not the main focus of this exercise.

- When I started this off, I began with implementing a simple API that serves the search results from github. This was most convenient because i would't have to bother with template rendering until i got to that point. Technically the API is not required, but it would be the way to go, if we wanted to add an AJAX-Layer for a nice-looking JavaScript frontend. I left it in there, eventhough the flask-restful requirement could be dropped without it.

- I was not extra cautious about handling errors. Although I handled all errors from github that i could perceive, and whatever i was expecting to probably fail. Still some dictionary lookups may fail if data structures vary. This was due to the fact, that this is only an assignment project, and github is known to be a `good web citicen`, so they wouldn't change their data structures inside one API version. For a production task i would come up with some more ways of data validation.

- I did not implement any tests for the project. This is of course also due to the fact, that tests were not required in the assignment.

- The github_search.py program library file can also be run standalone, for manual debugging. The code executed is at the end of the file and can be adapted to debugging needs.

- Overall I had a good time implementing this excercise. I will appreciate any feedback regarding it.
